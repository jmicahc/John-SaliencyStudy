import os
from Stimuli_Tool import Stimuli
import numpy as np
from scipy.stats import mstats

def getCond(ID, stimuli):
        for trial in stimuli:
            if ID == trial.data[0]:
                return '  '.join(trial.condition.split('_')[:-1])
        raise


if __name__ == '__main__':
    
    stim = Stimuli('../../Experiment/Materials/stimuli/')
    stimuli = stim.flat

    for filename in os.listdir('csv_files/'):
        if filename.startswith('.'): continue #ensure no hidden files
        if not filename.endswith('.csv'): continue #ensure correct file type.
        
        f_in = open('csv_files/'+filename)
        f_out = open('comparison_files/'+filename[:-4] + '_comp.' + 'txt', 'w')
        f_out.write('{:5}'.format('ID') + '{:10}'.format('Audio') + '{:24}'.format('Condition') + 
            '{:20}'.format('Interest_Area') + '{:9}'.format('Labeled?') + 
            '{:22}'.format('pts-in-poly') + '{:22}'.format('pts-total') + 
            '{:22}'.format('pts-in-all') + '{:22}'.format('Rel_Ratio') + 
            'Total_Ratio' + '\n')

        original = [line.split() for line in f_in]
    
    
        movie_starts = [i for i, l in enumerate(original) if 'MovieStart' in l]
        movie_ends = [i for i, l in enumerate(original) if 'MovieEnd' in l]
        zipped_movies = zip(movie_starts, movie_ends)
      

        #this crazy stuff exists due to a couple of mistakes in the experiment (I'm not quite sure what happened)
        #Basicallu I'm excluding one trial because it shows up twice in the experiment data.
        if 'Carla' in filename or 'Sarah' in filename:
            image_starts = [i for i, l in enumerate(original) if 'ImageStart' in l and '261' not in l]
            image_ends = [i for i, l in enumerate(original) if 'ImageEnd' in l and '262' not in l]
        else:
            image_starts = [i for i, l in enumerate(original) if 'ImageStart' in l and '259' not in l]
            image_ends = [i for i, l in enumerate(original) if 'ImageEnd' in l and '260' not in l]

        
        zipped_images  = zip(image_starts, image_ends)
        polygons=[]
        distributions = []

        #Loop through polygon names at the begining of file and add to a list.
        for item in original[0]:
            if 'AOI' in item:
                #print filename, item
                if item=='AOI[012_foot_': item = 'AOI[012_foot_]Hit' #fix labeling error
                if item=='AOI[081_sock_': item = 'AOI[081_sock_5]Hit' #fix labeling error
                if item==']Hit': continue #fix labeling error
                
                parsed = item[4:item.index(']Hit')]
                polygons.append(parsed)


        #In this for loop I recreate the order of the experiment by sorting
        #zipped image and movie trials. This works because zipped_movies and zipped_images
        #are just lists of tuples containing start and stop row indices for the trial, and
        #those are automatically sorted into original order by the sorted() function. 
        for start, stop in sorted(zipped_movies + zipped_images):
      
            mid = (start + stop) / 2

            trial = [line for line in original[mid:stop] if 'Fixation' in line and ('0' in line or '1' in line)]
            cleaned = [[item for item in line if item=='1' or item=='0'] for line in trial]
            if cleaned==[]:
              print filename
              print mid, original[start][0]
              print trial, '\n'
              continue


            #print cleaned
            labels = [polygons.pop(0) for i in range(len(cleaned[0]))]
            
            if min([len(l) for l in cleaned]) < len(cleaned[0]): 
              print "problem sir!"
              print cleaned
              print cleaned[0]
              print mid, stop, min([len(l) for l in cleaned]) 
            summed = [sum([int(line[i]) for line in cleaned]) for i in range(len(cleaned[0]))]
            zipped = zip(labels, summed)
            total = len(cleaned)

            f_name = original[start][0]
            ID = (f_name.split('_')[0], 'silent') if '.avi' not in f_name else (f_name.split('_')[1][:3], 'sound')

            for label, Sum in zipped:
              labeled = 0
              if '_L' in label:
                  labeled = 1
                  label = label[:-2]
              All = sum([int(Sum2) for label2, Sum2 in zipped])
              try: 
                rel_ratio = float(Sum) / float(All)
              except:
                rel_ratio = 0
                pass

              total_ratio = float(Sum) / float(total)
              distributions.append([Sum, total, All, rel_ratio, total_ratio])

              f_out.write('{:5}'.format(ID[0]) + '{:10}'.format(ID[1]) + 
                  '{:24}'.format(getCond(ID[0], stimuli)) + '{:20}'.format(label) + 
                  '{:9}'.format(str(labeled)) + '{:22}'.format(str(Sum)) + 
                  '{:22}'.format(str(total)) + '{:22}'.format(str(str(All))) + 
                  '{:22}'.format(str(rel_ratio)) + str(total_ratio) + '\n')



        print "distributions", filename, distributions
        dist = np.array(distributions)
        std_dev = np.std(dist, axis=0)
        mean = np.mean(dist, axis=0)
        median = np.median(dist, axis=0)
        mode = mstats.mode(dist, axis=0)[0][0]
        print mode

        f_out.write('\n' + '{:68}'.format('Standard_Deviations') + '{:22}'.format(str(std_dev[0])) + 
            '{:22}'.format(str(std_dev[1])) + '{:22}'.format(str(str(std_dev[2]))) + 
            '{:22}'.format(str(std_dev[3])) + str(std_dev[4]) + '\n')

        f_out.write('{:68}'.format('Mean') + '{:22}'.format(str(mean[0])) + 
            '{:22}'.format(str(mean[1])) + '{:22}'.format(str(str(mean[2]))) + 
            '{:22}'.format(str(mean[3])) + str(mean[4]) + '\n')

        f_out.write('{:68}'.format('Median') + '{:22}'.format(str(median[0])) + 
            '{:22}'.format(str(median[1])) + '{:22}'.format(str(str(median[2]))) + 
            '{:22}'.format(str(median[3])) + str(median[4]) + '\n')

        f_out.write('{:68}'.format('Mode') + '{:22}'.format(str(mode[0])) + 
            '{:22}'.format(str(mode[1])) + '{:22}'.format(str(str(mode[2]))) + 
            '{:22}'.format(str(mode[3])) + str(mode[4]) + '\n')






