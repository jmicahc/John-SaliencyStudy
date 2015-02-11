from src.saliency_map import SaliencyMap
from src.utils import OpencvIo
from Stimuli_Tool import Stimuli
import cv, cv2

#This is a python to create saliency maps based upon Itti and Koch (2000).
#This does not implement the GBVS algorithm.


#This is an arbitary matrix scalar that seems to work about right for create viewable
#png images. The saliency map output by the algorithm is a normalized matrix with elements
#between 0 and 1. This scales the matrix so that it can be viewed as a PNG image. If you want
#the normalized map, set this to 1.


SCALAR = 300

stimuli = Stimuli('Experiment/Materials/stimuli/')


for stim in stimuli.flat:

    oi = OpencvIo()
    src = oi.imread(stim.path)
    print "creating saliency map for. . .", stim.filename
    sm = SaliencyMap(src)
    sm.map = sm.map*SCALAR
    cv2.imwrite('Salience_Stills/'+stim.filename, sm.map)

