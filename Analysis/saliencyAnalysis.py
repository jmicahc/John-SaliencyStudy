from PIL import Image
from verticesTool import Complex_Polygon
from Stimuli_Tool import Stimuli, Trial
from psychopy import visual
import numpy as np
import os

# This script calculates the heat of each
# polygon. Area and centroid are also transfered over
# from the dependent text file (see below). Any
# gray-scale image can be used.
#
# Depends upon polygon_data.txt which can be found in the 
# Polygon_Data directory.
#
# Note that this scripts runs extremely slow (on my computer).
# It took me about 3 hours to run ~127 polygons.
#
# INPUTS:
#       polygon_data.txt (in Polygon_Data)
#       Saliency Images (in Saliency_Images/all) <-- should be modified to be in aguments
#
# OUTPUTS:
#       polygon_data2.txt (in Polygon_Data)
#       analysis_data.txt (in Polygon_Data)
#


def _toFile(image_data):
    f = open('Polygon_Data/analysis_data.txt', 'a')
    f.write(str(image_data) + '\n')
    
def getHeats(polygons, im):
    heats = [0] * len(polygons)
    totalHeat = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixel = im.getpixel((x, y))
            for i, p in enumerate(polygons):
                if p.contains((x, y)):
                    heats[i] += pixel
                totalHeat += pixel


    print heats, totalHeat
    return heats, totalHeat
                      
      
def translate(verts):
    for i in range(len(verts)): 
        verts[i][0] = verts[i][0] + 320 
        verts[i][1] = abs(verts[i][1] - 240)
    return verts

if __name__ == '__main__':

    
    polygons = {}
    win = visual.Window()

    #Create a dictionary with IDs as keys and lists of Complex_Polygons as
    #values. All data necessary for this is stored in polygon_data.txt.
    #A dicitonary is a prefered data structure in this case since 
    #it tends to be fault tolerant. 
    for line in open('Polygon_Data/polygon_data.txt'):
        line = line.strip()
        data = line.split("  ")
        while '' in data: data.remove('')
        cond = data[0]
        ID = data[1].strip()
        print line
        item = data[2]
        if item=='025_raceCar_2': continue #this polygon is seg-faulting after the translation.
        if '003_hand_6' in item: continue #also seg faulting. Should be redefined and then this line removed.
        centroid = eval(data[3])
        area = eval(data[4])
        verts = eval(data[5])

        #translate vertices to coorinate system with origin at top left (not center).
        verts = translate(verts)

        print verts
        if ID in polygons.keys():
            polygons.get(ID).append(Complex_Polygon(win, vertices=verts, label=item))
        else:
            polygons.update({ID : [Complex_Polygon(win, vertices=verts, label=item)]})
    

    #Create a dictioanry of images with agian trial ID as keys and the PIL.Image
    #objects as values. 
    images = {} 
    saliency_images = Stimuli('Saliency_Maps/')
    for trial in saliency_images.flat:
        im = Image.open(trial.path)
        images.update({trial.data[0] : im})


    #Run analysis on the list of polygons defined for each image. If a list of 
    #polygons is found for which there is no associated image, then skip it.
    image_data = {}
    print polygons
    for ID in polygons:
        print ID
        print polygons.keys()
        print images.keys()
        if not (ID in polygons.keys() and ID in images.keys()): continue
        print "found match"
        polys = polygons[ID]
        image = images[ID]

        labels = [poly.getLabel() for poly in polys]
        print labels
        centroids = [poly.getCentroid() for poly in polys]
        areas = [poly.getArea() for poly in polys]
        heats, totalHeat = getHeats(polys, image)
        _toFile({ID : (zip(labels, centroids, areas, heats), totalHeat)})
        image_data.update({ID : (zip(labels, centroids, areas, heats), totalHeat)})
        print image_data

    win.close()
    f = open('Polygon_Data/analysis_data2.txt', 'w')
    f.write(str(image_data))
    print '*******************************\nImage data\n', image_data
