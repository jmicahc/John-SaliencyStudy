from psychopy import event, core, visual
from collections import OrderedDict
from Stimuli_Tool import Stimuli, Trial
import random

#Generates a random ordering with all the constraints we talked about.
#The randomization code may not be the most inteligible, and it will
#ussually fail given the current constraints (since sometimes randomly
#assignming half of the trials to the first half of the experiment makes
#it impossible to meet all the constraints). However, this will work ~15%
#of the time.


def toFile(stim1, stim2):
    f = open('ordered_trials_test.txt', 'w')
    for trial in stim1:
        f.write('{:30}'.format(trial.condition))
        f.write('{:8}'.format(trial.data[0]))
        f.write('{:8}'.format(trial.data[1]))
        f.write('{:8}'.format(trial.data[3]))
        item = trial.data[2].split('+')
        f.write('{:15}'.format(item[0]))
        f.write('{:15}'.format(trial.path))
        f.write('\n')
    f.write("second half\n")
    for trial in stim2:
        f.write('{:30}'.format(trial.condition))
        f.write('{:8}'.format(trial.data[0]))
        f.write('{:8}'.format(trial.data[1]))
        f.write('{:8}'.format(trial.data[3]))
        item = trial.data[2].split('+')
        f.write('{:15}'.format(item[0]))
        f.write('{:15}'.format(trial.path))
        f.write('\n')


if __name__ == '__main__':
    pic_stim = Stimuli('Materials/stimuli/')
    pic_stim.shuffleBins()

    first_half = {}
    second_half = {}
    for cond_name in pic_stim.bins:
      if 'Silent' in cond_name:
        second_half.update({cond_name : pic_stim.bins[cond_name][:len(pic_stim.bins[cond_name])/2]})
        first_half.update({cond_name : pic_stim.bins[cond_name][len(pic_stim.bins[cond_name])/2:]})
      if 'Sound' in cond_name:
        first_half.update({cond_name : pic_stim.bins[cond_name][:len(pic_stim.bins[cond_name])/2]})
        second_half.update({cond_name : pic_stim.bins[cond_name][len(pic_stim.bins[cond_name])/2:]})

    first = pic_stim.randomize(first_half)
    second = pic_stim.randomize(second_half)

    toFile(first, second)
