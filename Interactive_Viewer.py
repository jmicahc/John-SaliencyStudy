from psychopy import visual, core, event
from sys import path
from Stimuli_Tool import Stimuli
import os
import shutil
path.insert(1, '/home/john/Python_Environments/video_analysis/lib/python2.7/site-packages')
from psychopy import gui

# This is a tool for visualizing the stimuli with the associated saliency
# map and video clip. You can step forward and backrward through stimuli,
# save images, and navigate frame-by-frame.
#
# ACTIONS:
#     - 'n' --> next image
#     - 'p' --> previous image
#     - 'f' --> enter frame-by-frame mode
#     - 'space' --> pause/start
#     - 'u' --> update (draws everything)
#     - 'r' --> step back 3 seconds
#     - 'j' --> step forward 3 seconds
#
 


def saveNewImage(mov, frame):
    '''
    ----INCOMPLETE-----
    Saves an image captured during frame-by-frame mode and
    adds it to the directory all_stills_current, which contains
    all of the stills used in the study. Input boxes will pop up
    asking user to "code" the image.
  
    IMPUTS: (object) movie
            urrently
                  non-functional
    INPUT:
          (Object) movie
          (float) current timestamp
    OUTPUTS:
          None
    '''
    win.getMovieFrame()
    image_data = {'Name':'','Condiion':'','Language':'','Items':'','Time':'', 'ID': 0}
    infoDlg = gui.DlgFromDict(dictionary=image_data, title='Picture Data',
        fixed = [])
    if infoDlg.OK:
        print image_data
    else:
        print 'User Cancell'
    win.saveMovieFrames('frame' + str(image_data.get('ID')) + '.png')

def frameByFrame(mov, frame):
    mov.play()
    while mov.status != visual.FINISHED:
        for key in event.getKeys():
            if key in ['n']:
                mov.draw()
                win.flip()
            elif key in ['b']:
                return
            elif key in ['r']:
                print 'seeking frame:', frame
                mov.seek(frame)
                mov.play()
                win.flip()
            elif key in ['s']:
                saveNewImage(mov, frame)



if __name__ == '__main__':

  win = visual.Window([640,480])
  picWin = visual.Window([640,600], pos=(0,0))
  salWin = visual.Window([700, 500], pos=(0,1))
  #summaryWin = visual.Window([400, 400], pos=(0,0))

  globalClock = core.Clock()

  #Change the directory specified here if you want to use different stimuli,
  #just make sure the folder naming convention follows the folders at the 
  #end of the paths here.
  images = Stimuli('Experiment/Materials/stimuli/')
  movies = Stimuli('Experiment/Materials/movies/')
  sal_images = Stimuli('Materials/gbvs_stills/')


  image = visual.ImageStim(picWin)
  salImage = visual.ImageStim(salWin)
  text = visual.TextStim(picWin, pos=(0.0, -0.9), wrapWidth=1.0, height=0.04)
  picWin.flip()
  salWin.flip()


  i = 0
  while i < len(images.flat):
      pic = images.flat[i]


      #load subject video
      mov = visual.MovieStim(win, movies.bins[pic.data[1]][0].path)
      
      #start video from picture onset time
      frame = pic.data[3]
      mov.seek(frame)
      mov.play()

      #Dislay current picture 
      image.setImage(pic.path)
      text.setText(pic.filename) 
      image.draw()
      text.draw()
      picWin.flip()

      #Display Saliency Map of current Picture
      try:
          sal_image_path = sal_images.getTrial(pic.data[0]).path
          print sal_image_path
          salImage.setImage(sal_image_path)
          salImage.draw()
          salWin.flip()
      except:
          print "Saliency map could not be found. Continuing"
          pass
      
      while mov.status != visual.FINISHED:
          mov.draw()
          win.flip()
          end = False
          for key in event.getKeys():
              if key in ['escape','q']:
                  win.close()
                  core.quit()
              elif key in ['enter', 'return']: # enter --> go to next image
                  mov.pause()
                  end = True
                  break
              elif key in ['f']: # f --> switch to frame-by-frame mode
                  frameByFrame(mov, frame)
              elif key in ['r']: # r --> reverse
                  mov.seek(frame - 3)
                  mov.play()
              elif key in ['j']: # j --> jump forward
                  mov.seek(frame + 3)
                  mov.play()
              elif key in ['p']: # p --> previous image
                  i -= 2
                  end = True
                  break
              elif key in ['u']: # u --> update (i.e. draw everything)
                  text.draw()
                  picWin.flip()
                  salImage.draw()
                  salWin.flip()
              elif key in ['space']:
                  print visual.PAUSED, visual.PLAYING
                  if (visual.PAUSED==2):
                      mov.pause()
                      visual.PAUSED = 1
                  else: 
                      mov.play()
                      visual.PAUSED = 2
          if end:
              break
      prevFrame = frame
      i += 1


  picWin.close()
  salWin.close()
  win.close()
  core.quit()


