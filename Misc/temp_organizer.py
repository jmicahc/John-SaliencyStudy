#stript to organize image files
f = open('stills.txt', 'r')
f_out = open('organized.txt', 'w')
import os
import array

uid = 0
for line in f:
  line = line[45:]
  line = line.strip()
  

  
  print line
  t = line.split('_')
  try:
    temp = t[4]
    datpya[0].append(t[0]+str(uid)-'.png')
    data[1].append(item+str(t[1])
    data[2].append(t[2])
    data[3].append(t[3])
    data[4].append(temp[:len(temp)-4]))

#    f_out.write('{0:<10}'.format(t[0]+str(uid)+'.png'))
#    f_out.write('{0:<15}'.format(t[1]))
#    f_out.write('{0:<15}'.format(t[2]))
#    f_out.write('{0:<40}'.format(t[3]))
#    f_out.write('{0:<15}'.format(temp[:len(temp)-4]))

    temp = 60*60*float(line[len(line)-10:len(line)-9])
    temp += 60*float(line[len(line)-7:len(line)-5])
    temp += float(line[len(line)-7:len(line)-5])
    data[5].append(temp)
 
#    f_out.write('{0:<15}'.format(temp))
#    f_out.write('\n')
  except :
    f_out.write('\n')
    print 'error durring formatting... file name inccorect'
  uid += 1

for column in d
  


