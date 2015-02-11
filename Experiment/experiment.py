from psychopy import event, core, visual
from Stimuli_Tool import Stimuli, Trial
import random
import pyglet

#This is the experiment. Loads stimuli based
#upon ording in ordered_trials.txt and displays
#each one for 5 seconds, with 1.5 secnods between them.
#To quit, press 'q'.

def main():

    sound_stim = Stimuli('Materials/audio/')
    sound = pyglet.media.Player()

  
    win = visual.Window(([1366, 768]),fullscr=True)
    pic = visual.ImageStim(win)


    for i, trial in enumerate(open('ordered_trials.txt')):
        data = trial.split()
        cond = data[0]
        ID = data[1]
        movie = data[2]
        onset = int(data[3])
        location = data[5]


        audio = True if 'Sound' in cond else False
        if True:
            onset = onset - 2
            print movie
            audio_file = pyglet.resource.media(sound_stim.bins[movie][0].path)
            print audio_file
            sound.queue(audio_file)
            if i > 0: sound.next()
            sound.seek(onset)
            
        #set picture stimuli
        pic.setImage(location)
        pic.draw()
        win.flip()

        timer = core.CountdownTimer(6.5)
        while timer.getTime() > 0:
            if audio: sound.play()
            if timer.getTime() < 1.5:
                sound.pause()
                win.flip()
            for key in event.getKeys():
                if key in ['q']:
                    quit = True
                    return
    win.close()

if __name__ == '__main__':
    main()
