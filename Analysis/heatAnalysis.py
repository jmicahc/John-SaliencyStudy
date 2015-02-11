from Stimuli_Tool import Stimuli

# This script processes the heat in each polygon relative to the sum of the heat 
# in all the polygons in the image (called rel_ratio), and processes the heat
# for each polygon relative to the total heat in the image (called total_ratio).
# These quantities, as well as the polygons name, area, and centroid are written
# to a file called gbvs_data_temp.txt which can be found in the Polygon_Data folder.
# The expectation is that the user rename this file once the file is created so that
# it is not accidentally overwritten if the program is rerun.
#
#
# "Heat" in an interest area is defined as simply the sum of the pixel values in the region.
# saliencyAnalysis.py is used to calculate the heat. This just formats the data and computes
# proportions.
#
# Note that this script depends upon the file called analysis_data2.txt which can
# be found in the folder Polygon_Data
#
# INPUTS:
#     - Polygon_Data/analysis_data2.txt
# 
# OUTPUTS:
#      - Polygon_Data/gbvs_data_temp.txt
#           **it is commended to create a
#             copy of this file  when created
#             so it is not accidentally 
#             overwritten.


def getCond(ID, stimuli):
    for trial in stimuli:
        if ID == trial.data[0]:
            return trial.condition
    raise
    



if __name__ == '__main__':
    f = open('Polygon_Data/analysis_data2.txt')
    for line in f:
      all_data = eval(line.strip())

    #Note this will overwrite an existing file!
    f_data = open('Polygon_Data/gbvs_data_temp.txt', 'w')
    stim = Stimuli('../Experiment/Materials/stimuli/')
    stimuli = stim.flat    


    for ID in all_data:
      image_data = all_data[ID]
      polygons = set(image_data[0])
      totalHeat = image_data[1]
      
      data_out = []

      for polygon in polygons:
          cond = getCond(ID, stimuli)
          name = polygon[0]
          centroid = polygon[1]
          area = polygon[2]
          print ID, cond, name, centroid, area

          All = polygons.copy()

          #proportion of heat inside polygon relative to sum of heat in all polygons.
          rel_ratio = float(polygon[3]) / float(sum([p[3] for p in All]))

          #Proportion of heat relative to total image.
          total_ratio = float(polygon[3]) / float(totalHeat)

          
          #Each polygon has an ID which is defined in the polygon's name, which
          #follows the form, trial-ID_name_poly-ID. E.g. 003_hand_2. Thus,
          #trial-ID plus poly-ID can uniquely determine a polygon.
          name_data = name.split('_')
          poly_ID = name_data[2]

          f_data.write('{:5}'.format(str(ID)) + '{:32}'.format(cond) + 
              '{:23}'.format(name.strip()) + '{:8}'.format(poly_ID) + 
              '{:23}'.format(str(rel_ratio)) + '{:23}'.format(str(total_ratio)) + 
              '{:15}'.format(str(centroid)) + '{:18}'.format(area) +'\n')





