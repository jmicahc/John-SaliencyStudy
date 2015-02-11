import os
import sys
import shutil



def main():
    for d in os.listdir('stimuli/'):
      for filename in os.listdir('stimuli/' + d):
        data = filename.split('_')
        ID = data[0]


        old_file = ''
        for fname in os.listdir('images/'):
          fdata = fname.split('_')
          fID = fdata[0]
          if ID == fID:
              print ID, fID
              data.insert(1, fdata[1])
              old_file = fname

        print 'stimuli/' + d + filename
        print 'stimuli/' + d + old_file
        shutil.copyfile('images/' +filename, 'stimuli/' + d + '/' + old_file)
        
        




if __name__ == '__main__':
    main()
