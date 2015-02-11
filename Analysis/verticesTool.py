from psychopy import visual, event, core
from Stimuli_Tool import Stimuli, Trial
import numpy
import psychopy
import sys
import os
import datetime
from p2t import CDT, Point, Triangle

#This is the script used to define interest areas. Bare in mind that it
#is somewhat buggy, though largely functional. The biggest issue is an
#underlying bugg in pygame which causes segfaults when certain vertices are used
#to define a polygon. There is probably not really a fix for this. 
#
# ACTIONS:
#     - click on points to define interest areas.
#     - click on interest areas to rename or delete them.
#     - press 's' to save polygons defined so far to polygon_data.txt.
#     - press 'd' to save a polygon when you are done defining vertices.
#     - press 'n' to go onto the next image. Also saves current vertices as a polygon, if any exist.
#     - press 'b' to unto the most recent vertex defined.
#     - press 'q' to save all polygons and quit.
#
# FILES USED:
#     - polygon_data.txt (INPUT) <-- stores the ordered vertices, area, centroid, ID, and name of every polygon.
#       When this script is run, this file is read though and all the polygons defined in it are loaded and
#       displayed when you get to their associated image. I recomend making a backup of polygon_data.txt every
#       once and a while to ensure that you don't run risks of losing a lot of data. Or just build back-up functionality
#       into this script.
#
#
from psychopy import gui




class Complex_Polygon():

    def __init__(self, win, units='pix', lineWidth=1.0, lineColor=(1.0,1.0,1.0), lineColorSpace='rgb',
            fillColor=None, fillColorSpace='rgb', vertices=((-50,0),(50,0),(100,0)), 
            closeShape=True, pos=(0,0), size=1, ori=0.0, opacity=1.0, contrast=1.0,
            depth=0, interpolate=True, lineRGB=None, fillRGB=None, name=None,autoLog=None, label=''):


        self.win = win
        self.units=units
        self.lineWidth=lineWidth
        self.lineColor=lineColor
        self.lineColorSpace=lineColorSpace
        self.fillColor=fillColor
        self.fillColorSpace=fillColorSpace
        self.vertices=vertices
        self.closeShape=closeShape  
        self.pos=pos
        self.ori=ori
        self.size=size
        self.opacity=opacity
        self.contrast=contrast
        self.depth=depth
        self.interpolate=interpolate
        self.lineRGB=lineRGB
        self.fillRGB=fillRGB
        self.name=name
        self.autoLog=autoLog
        self.label=label

        self.points = []
        for vert in self.vertices:
            self.points.append(Point(vert[0], vert[1]))

        self.triangles = []
        if len(self.vertices)>2:
            cdt = CDT(self.points)
            tmp_triangles = cdt.triangulate()
            for t in tmp_triangles:
                pts = [t.a,t.b,t.c]
                self.triangles.append(self._newPolygon(pts))
        else:
            if not self.points:
                self.triangles.append(self._newPolygon([Point(0,0)]))
            else:

                self.triangles.append(self._newPolygon(self.points))

    def __str__(self):
          string = '{:20}'.format(self.getLabel())
          string +=  '{:15}'.format(str(self.getCentroid()))
          string += '{:13}'.format(str(self.getArea()))
          #for i in range(len(self.vertices)):                     # Note this needs to be uncommented if you are using heatAnalysis.py, and comented otherwise.
          #    self.vertices[i][0] = self.vertices[i][0] + 320 
          #    self.vertices[i][1] = abs(self.vertices[i][1] - 240)
          string += str(self.vertices)
          return string

    def _recurse(self):
        self.__init__(self.win, units=self.units, lineWidth=self.lineWidth,
          lineColor=self.lineColor, lineColorSpace=self.lineColorSpace, fillColor=self.fillColor,
          fillColorSpace=self.fillColorSpace, vertices=self.vertices, closeShape=self.closeShape,
          pos=self.pos, size=self.size, ori=self.ori, opacity=self.opacity, contrast=self.contrast,
          depth=self.depth, interpolate=self.interpolate,lineRGB=self.lineRGB, fillRGB=self.fillRGB,
          name=self.name, autoLog=self.autoLog, label=self.label)



    def _newPolygon(self, points):
      '''
      creates a new ShapeStim triangle with values given during init.
      '''
      points_list = []
      for point in points:
          points_list.append((point.x, point.y))
      return visual.ShapeStim(self.win, units=self.units, lineWidth=self.lineWidth,
          lineColor=(1.0,1.0,1.0), lineColorSpace='rgb', fillColor=self.fillColor,
          fillColorSpace='rgb', vertices=points_list, closeShape=self.closeShape,
          pos=self.pos, size=self.size, ori=self.ori, opacity=self.opacity, contrast=self.contrast,
          depth=self.depth, interpolate=self.interpolate,lineRGB=self.lineRGB, fillRGB=self.fillRGB,
          name=self.name, autoLog=self.autoLog)

    def contains(self, point):
      for triangle in self.triangles:
        if triangle.contains(point):
          return True
      return False

    def draw(self):
      for triangle in self.triangles:
         triangle.draw()
  
    def setFillColor(self, color, colorSpace=None, log=None):
      for triangle in self.triangels():
        triangle.setFillColor(color, colorSpace, log)

    def setOpacity(self, newOpacity, operation='', log=None):
      for triangle in self.triangles:
        triangle.setOpacity(newOpacity, operation, log)

    def getArea(self):
        #Implements the AFAIK method for computing the area of a 2D
        #polygon. Sums the cross products around each vertex.
        #Taken from: http://stackoverflow.com/questions/451426/
        #  how-do-i-calculate-the-surface-area-of-a-2d-polygon
        if self.vertices != []:
            return 0.5 * abs(sum(x0*y1 - x1*y0
                         for ((x0, y0), (x1, y1)) in self._segments(self.vertices)))
        else:
            return None
    def _segments(self, p):
        return zip(p, p[1:] + [p[0]])
        
    def getCentroid(self):
        # cetroid is defined as (ave(xi), ave(yi)) in 2D space.
        # convert to form c = [[x1, x2, x4 ...], [y1, y2, y3 ...]]
        # and express each vertex of the centroid as sum(c[i]/len(c[i]))
        if self.vertices != []:
            xList = [c[0] for c in self.vertices]
            yList = [c[1] for c in self.vertices]
            return (sum(xList)/len(xList), sum(yList)/len(yList))
        else:
            return None

    def setVertex(self, vert):
      self.vertices.append(vert)
      self._recurse()

    def popVertex(self):
        try:
            self.vertices.pop()
        except:
            pass
        self._recurse()
    
    def getPoints(self):
        return self.points
    
    def getLabel(self):
        return self.label

    def setLabel(self):
        dlg = gui.Dlg("Interest Area Name")
        dlg.addField("Name", self.label)
        dlg.addField('Delete?', choices=["No", "Yes"])
        dlg.show()
        if dlg.OK:
            self.label = dlg.data[0]
        else:
            return None
        return dlg.data

def _toFileBuffer(ID, poly):
    f = open('.poly_data_buffer.txt', 'a')
    for ID in polys:                   
        if polys[ID][0].getCentroid()==None: continue
        f.write('{:10}'.format(str(ID)))
        f.write(str(polys[ID]))
        f.write('\n')
    f.close()



def _toFile(all_polys):
    f = open('Polygon_Data/polygon_data.txt', 'w')
    print "saving polygons"
    for ID in all_polys:
        for poly in all_polys[ID]:
            if poly.getCentroid() == None: continue
            f.write('{:6}'.format('test'))
            f.write('{:10}'.format(str(ID)))
            f.write(str(poly))
            f.write('\n')


def _loadData(win, filename):
    f = open(filename, 'r')
    all_polys = {}
    for line in f:
        items = line.split("  ")
        while '' in items: items.remove('')
        if len(items) < 6:
            continue
        ID = items[1].strip()
        verts = eval(items[5])
        label = items[2]
        if ID in all_polys:
            all_polys[ID].append(Complex_Polygon(win, vertices=verts, fillColor='red', opacity=0.3, label=label))
        else:
            all_polys.update({ID : [Complex_Polygon(win, vertices=verts, fillColor='red', opacity=0.3, label=label)]})

    return all_polys


def _drawAll(image, text, all_polys, ID, win):
    image.draw()
    for poly in all_polys[ID]:
        poly.draw()
    text.draw()
    win.flip()

def _addPoly(all_polys, poly, ID):
    if ID in all_polys:
        all_polys[ID].append(poly)
    else:
        all_polys.update({ID : [poly]}) 
    #_toFileBuffer(ID, poly)

def _main():

    win = visual.Window([640, 480], units='pix')
    winShape = visual.ShapeStim(win, units='norm', vertices=((1,1), (-1, 1), (-1, -1), (1, -1)))
    mouse = event.Mouse(win=win)

    all_polys = _loadData(win, 'Polygon_Data/polygon_data.txt')
    
    stim =  Stimuli('Interest_Areas/')

    for trial in stim.flat:
        if not trial.filename.endswith('.png'):
            continue


        ID = trial.data[0]

        image = visual.ImageStim(win, trial.path)
        text = visual.TextStim(win, units='norm', pos=(0.0, -0.8), text=trial.filename, color='black') 
        
        polygon = Complex_Polygon(win, vertices=[], fillColor='red', opacity=0.3)
        _addPoly(all_polys, polygon, ID)
        _drawAll(image, text, all_polys, ID, win)

        while True:
 
          if mouse.isPressedIn(winShape):
              x_y = mouse.getPos()
              x_y = x_y.tolist()

              #select polygon to modify if they are clicked on
              for poly in all_polys[ID]:
                  if poly == polygon: continue
                  if poly.contains(x_y):
                      rsps = poly.setLabel()
                      if rsps==None: break
                      if rsps[1] == "Yes": all_polys[ID].remove(poly)
                      break
              else:
                  polygon.setVertex(x_y)
              _drawAll(image, text, all_polys, ID, win)

              while mouse.getPressed() != [False, False, False]: continue

          for key in event.getKeys():
              if key in ['q']: 
                  _toFile(all_polys)
                  return
              elif key in ['d']:
                  polygon.setLabel()
                  polygon = Complex_Polygon(win, vertices=[],fillColor='red',opacity=0.3)
                  _addPoly(all_polys, polygon, ID) 
              elif key in ['n']:
                  _toFile(all_polys)
                  win.getMovieFrame()
                  _addPoly(all_polys, polygon, ID) 
                  break
              elif key in ['b']:
                  polygon.popVertex()
                  _drawAll(image, text, all_polys, ID, win)
              elif key in ['s']:
                  _toFile(all_polys)
          else:
            continue
          break
              
    win.close()

if __name__ == '__main__':
    _main()

