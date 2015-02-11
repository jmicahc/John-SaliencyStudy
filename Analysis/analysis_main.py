import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def flatten(x):
    '''
    Flattens an n-dimentional list and returns a 
    one dimentional list composed of all the elements
    in the orgiginal list.
    '''
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

class Gbvs_Poly():
  '''
  Just a bunch of fields storing infomration about a polygon defined over
  a GBVS image.
  '''

  def __str__(self):
      return str(self.ID) + '  ' + str(self.poly_ID) + '  ' + str(self.cond) + '  ' + self.name 

  def __init__(self, data):
      while '' in data: data.remove('')
      self.cond = [item.lower() for item in data[1].split('_')]
      self.ID = int(data[0])
      self.name = data[2]
      self.poly_ID = float(data[3])
      self.rel_ratio = float(data[4])
      self.total_ratio = float(data[5])
      self.centroid = eval(data[6])
      self.area = float(data[7])
      self.labeled = True if '_L' in self.name else False


class Gbvs_Data():
  '''
  This class represents all the information gathered about the polygons, including
  their saliency data. Basically, it is for interactively using the Gbvs_Data.txt
  file.
  '''
  def __init__(self):
      self.polys = {}
  
  def addPoly(self, data):
    #Adds a polygion to the dictionary of polygon lists with
    #key value of the ID for the trial
    poly_pair = (Gbvs_Poly(data), Gbvs_Poly(data))
    poly_pair[0].ID += 100 #This is a werid fix due to the fact that I didn't uniquely ID all trials.
    poly_pair[0].cond[2] = 'sound' if poly_pair[0].cond[2]=='silent' else 'silent' #again, weird fix.
    for poly in poly_pair:
        if poly.ID in self.polys:
            gbvs.polys[poly.ID].append(poly)
        else:
            gbvs.polys.update({poly.ID : [poly]})

  def allPolys(self):
    '''
    Returns all the polygons as a list.
    '''
    return flatten(self.polys.values())


  def polysByCond(self, conds=[]):
      '''
      returns a list of polygons with condition levels matching
      those defined in *conds*. Matching proceeds only on those
      conditions for which *conds* is defined. Specifically,
      a trial is selected for the output list if the
      difference from *self.conds* and *conds* is the empty set.
      '''
      polygons = []
      for ID in self.polys:
          poly = self.polys[ID][0]
          print conds, poly.cond, set(conds) - set(poly.cond)
          if len(set(conds) - set(poly.cond))==0:
              polygons.append(poly)

      return polygons
 

  def findPoly(self, ID, poly_ID):
      '''
      Returns the polygon (*poly_ID*) in trial (*ID*)
      '''
      for poly in self.polys[ID]:
          if poly.poly_ID == poly_ID:
              return poly
      print "polygon not found", ID, poly_ID
      raise

  def hasPoly(self, ID, poly_ID):
      #returns true if a the polygon poly_ID at trial ID exists.
      #Otherwise returns false.
      try: #dangerous
          for poly in self.polys[ID]:
              if poly.poly_ID == poly_ID:
                  return True
          return False
      except:
          print "****************************************Could not find", ID, poly_ID, ". . . excluding"
          return False


class SubjectPoly():
    '''
    Represents an interest area.
    '''
    def __init__(self, data, sj_name):
        self.cond = [item.lower() for item in data[1:4]]
        self.ID = int(data[0]) + 100 if 'sound' in self.cond else int(data[0])
        self.label = data[4]
        self.poly_ID = float(data[4].split('_')[2])
        self.Sum = float(data[5])
        self.rel_ratio = float(data[9])
        self.total_ratio = float(data[10])
        self.labeled = True if '_L' in data[4] else False

class SubjectDiff():
    '''
    Data structure with fields for representing the difference from the saliency algorithm
    for one trial
    '''
    def __init__(self, ID, cond, expected, actual, labeled, poly_ID, rel_ratio, total_ratio, alg='gbvs'):
        self.ID = int(ID)
        self.cond = cond
        self.expected = expected
        self.actual = actual
        self.poly_ID = poly_ID
        self.labeled = labeled
        self.rel_ratio = float(rel_ratio)
        self.total_ratio = float(total_ratio)
        self.alg = alg

class SubjectData():
    '''
    Represents a subject in the experiment. A dictionary is used mapping from
    trial ID to to Sj
    '''
    def __init__(self):
        self.data = {}
        self.diffs = {}

    def polysByCond(self, conds=[]):
      #print "Conditions", conds
      polygons = []
      for ID in self.data:
          poly = self.data[ID][0]
          if len(set(conds) - set(poly.cond)) == 0:
              polygons.append(poly)

      return polygons

    
    def diffByCond(self, conds=[]):
        diffs = []
        for ID in self.diffs:
            diffs_cond = self.diffs[ID][0].cond
            if len(set(conds) - set(diffs_cond))==0:
                diffs += self.diffs[ID]

        return diffs
    
    def diffAsTrial(self, conds=[]):
        diffs = []
        for ID in self.diffs:
            diffs_cond = self.diffs[ID][0].cond
            if len(set(conds) - set(diffs_cond))==0:
                diffs.append([diff.rel_ratio for diff in self.diffs[ID]])

        return diffs


    def addDiff(self,ID, poly, expected, actual, rel_ratio, total_ratio):
        #if ID (trial) doesn't exist, create a new one and add a with an associated difference. Else
        #append to the existing list of polygons for the given ID.

        if ID in sj.diffs:
            sj.diffs[ID].append(SubjectDiff(ID, poly.cond, expected, actual, poly.labeled, poly.poly_ID, diff_rel, diff_total))
        else:
            sj.diffs.update({ID : [SubjectDiff(ID, poly.cond, expected, actual, poly.labeled, poly.poly_ID, diff_rel, diff_total)]})
        
      


if __name__ == '__main__':

    #build gbvs data structure. Consists of a dictionary with keys as trial IDs and
    #values as lists of polygon objects containing information about the polygon.
    gbvs_file = open('Polygon_Data/gbvs_data.txt')
    gbvs = Gbvs_Data()
    for line in gbvs_file:
        data = line.split('  ')
        gbvs.addPoly(data)


    ss_path = 'Subject_Data/txt_files/'
    subject_files = [open(ss_path + f) for f in os.listdir(ss_path) if f.endswith('.txt')]


    subjects = []
    #build subject data structures. A subject data structure consists of a map of
    #key-value pairs with trial IDs as keys and lists of interest area objects as 
    #values. Trials currently do not have their own data structure, but interest areas
    #have a field representing their associated condition.
    for sj_file in subject_files:
      sj = SubjectData()
      for line in sj_file:
          if len(line.strip())==0: continue
          if line.startswith('Standard'): break
          if line.startswith('ID'): continue

          print line.split()
          data = SubjectPoly(line.split(), sj_file)

          if data.ID in sj.data:
              sj.data[data.ID].append(data)
          else:
              sj.data.update({data.ID : [data]})
      
      subjects.append(sj)

   
    #Add comparision information to subject data structures and write comparision data to file 
    for sj, f in zip(subjects, subject_files):
        f_comparison_data = open('Subject_Data/comparison_files/'+f.name.split('/')[-1] , 'w')
        f_comparison_data.write('{:14}'.format('ID (trial)') + '{:30}'.format('Condition') + 
            '{:20}'.format('Expected_rel_others') + '{:20}'.format('Actual_rel_others') + 
            '{:20}'.format('Expected__rel_total') + '{:20}'.format('Actual_rel_total') + 
            '{:20}'.format('Diff_rel_others') + '{:20}'.format('Diff_rel_total') + '\n') 
        for ID in sj.data:
            for poly in sj.data[ID]: 
                if gbvs.hasPoly(ID, poly.poly_ID):
                    
                    #sum of pixel values inside polygon / sum of of pixel values in all polygons
                    expected_rel = gbvs.findPoly(ID, poly.poly_ID).rel_ratio

                    #Sum of pixel values inside polygon / sum of pixel values in the image.
                    expected_total = gbvs.findPoly(ID, poly.poly_ID).total_ratio

                    #Sum of fixations inside polygon (interest area) / sum of fixations in all polygons
                    actual_rel = poly.rel_ratio

                    #sum of fixations inside polygon / sum of fixations in second half of trial
                    actual_total = poly.total_ratio

                    #The differences between expected (gbvs algorithm) and actual (eye-tracking data)
                    diff_rel = abs(expected_rel - actual_rel)
                    diff_total = abs(expected_total - actual_total)

                    f_comparison_data.write('{:14}'.format(str(ID)) + '{:30}'.format(' '.join(poly.cond)) +
                        '{:20}'.format(str(expected_rel)) + '{:20}'.format(str(actual_rel)) + 
                        '{:20}'.format(str(expected_total)) + '{:20}'.format(str(actual_total)) +
                        '{:20}'.format(str(diff_rel)) + '{:20}'.format(str(diff_total)) + '\n')
                  

                    #Add difference to map of differnces. This map consists of key-value pairs with
                    #trial IDs as the keys and a list of polygons (interest areas) associated with 
                    #that trial as the values 
                    sj.addDiff(ID, poly, expected_rel, actual_rel, diff_rel, diff_total)

        


    #We can do analysis on specific conditions using these condition codes.
    #Condition codes with fewer than three entries can be defined if we 
    #want to select a subset of all conditions, rather than just one condition.
    M_L_A = ['multiitem', 'labelled', 'sound']
    M_N_A = ['multiitem', 'nonlabelled', 'sound']
    M_L_S = ['multiitem', 'labelled', 'silent']
    M_N_S = ['multiitem', 'nonlabelled', 'silent']
    O_L_A = ['oneitem', 'labelled', 'sound']
    O_N_A = ['oneitem', 'nonlabelled', 'sound']
    O_L_S = ['oneitem', 'labelled', 'silent']
    O_N_S = ['oneitem', 'nonlabelled', 'silent']


    # A bunch of analyses. Each is a list of lists, where the inner list consists of floating point 
    # numbers representing the absolute value of the difference between "expected" and "actual" for
    # one interest area. "Expected" is the proportion computed from the saliency algorithm. "Actual"
    # is the proportion computed from eye-tracking data. The analysis is done on a interest-area basis.
    # Slight modifications will be necesary if we want to do the analysis on a trial basis.
    # The average of each list expresses how closely eye-tracking data matches the saliency map. Lower 
    # values correspond to a closer fit, larger values corrpesond to weaker fit.
    #
    # ratio_diffs is a proportion computed relative to the sum of the heat in all interest areas
    # total_diffs is a proportion computed relative to the sum of the heat in the entire image.
    M_L_A_rel_ratio_diffs = np.array([[diff for diff in sj.diffByCond(M_L_A)] for sj in subjects])
    M_L_S_rel_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(M_L_S)] for sj in subjects])
    M_N_A_rel_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(M_N_A)] for sj in subjects])
    M_N_S_rel_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(M_N_S)] for sj in subjects])
    O_L_A_total_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(O_L_A)] for sj in subjects])
    O_L_S_total_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(O_L_S)] for sj in subjects])
    O_N_A_total_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(O_N_A)] for sj in subjects])
    O_N_S_total_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(O_N_S)] for sj in subjects])


    #Analysis of labeled vs. non-labeled interest areas for multiple item sound conditions. 
    M_L_A_labeled_IAs = []
    M_L_A_nonlabeled_IAs = []
    for diff in flatten(M_L_A_rel_ratio_diffs):
        if diff.labeled:
            M_L_A_labeled_IAs.append(diff.total_ratio)
        else:
            M_L_A_labeled_IAs.append(diff.total_ratio)
    print 'MEAN:', np.mean(M_L_A_labeled_IAs)
    print 'MEAN:', np.mean(M_L_A_nonlabeled_IAs)

    M_L_A_rel_ratio_diffs = np.array([[diff.total_ratio for diff in sj.diffByCond(M_L_A)] for sj in subjects])
            

    M_L_A_expected = np.array([poly.rel_ratio for poly in gbvs.polysByCond(M_L_A)])
    M_L_A_actual = np.array([[poly.rel_ratio for poly in sj.polysByCond(M_L_A)] for sj in subjects])

    M_N_A_expected = np.array([poly.rel_ratio for poly in gbvs.polysByCond(M_N_A)])


    M_N_A_actual = np.array([poly.rel_ratio for poly in sj.polysByCond(M_N_A)])

    #print "Mean expected:", np.mean(M_L_A_expected)
    #print 'Mean actual', np.mean(M_L_A_actual), '\n'

    differences = (np.mean(M_L_A_rel_ratio_diffs), np.mean(M_N_A_rel_ratio_diffs), np.mean(M_L_S_rel_ratio_diffs))
    stds = (np.std(M_N_A_rel_ratio_diffs), np.std(M_N_A_rel_ratio_diffs), np.std(M_L_S_rel_ratio_diffs))
    ind = np.arange(len(differences))
    width = 0.35
    p1 = plt.bar(ind, differences, width, color='r', yerr=stds)
    plt.show()
   
    #print np.mean(M_L_A_rel_ratio_diffs)
    #print np.std(M_L_A_rel_ratio_diffs)
    #print np.mean(M_N_A_rel_ratio_diffs)
    #print np.std(M_L_A_rel_ratio_diffs)
    #print np.mean(M_L_S_rel_ratio_diffs)

    #print '\n', np.mean(O_L_A_total_ratio_diffs)
    #print np.mean(O_N_A_total_ratio_diffs)
    #print np.mean(O_L_S_total_ratio_diffs)

    #print ttest_ind(flatten(M_L_A_rel_ratio_diffs), flatten(M_N_A_rel_ratio_diffs))



    data = []
    for i, diff in enumerate(flatten([sj.diffByCond(M_N_A) for sj in subjects])):
        data += [(i, i), (diff.actual, diff.expected), 'r']

    data2 = []
    for i, diff in enumerate(flatten([sj.diffByCond(M_L_A) for sj in subjects])):
        data2 += [(i, i), (diff.expected, diff.actual), 'g']
        
    plt.plot(*data)
    plt.plot(*data2)
    plt.show()

    M_labeled = []
    M_nonlabeled = []
    for poly in gbvs.allPolys():
        if poly.labeled:
            M_labeled.append(poly.area)
        else:
            M_nonlabeled.append(poly.area)
    
    #plt.plot(np.arange(len(gbvs.allPolys()))*2, [poly.area for poly in gbvs.allPolys()], '.r-')
    #plt.show()

            

    #M_L_A_areas_mean = np.mean([poly.area for poly in gbvs.allPolys()])
    #M_N_A_areas_mean = np.mean([poly.area for poly in gbvs.polysByCond(M_N_A)])
    #print M_L_A_areas_mean, M_N_A_areas_mean
  





    





    



                





         
          
