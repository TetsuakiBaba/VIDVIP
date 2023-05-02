import glob
import re
import os
import csv
import copy

remove_annotation_number = 35
file = glob.glob('all/*.txt')

for f_each in file:
        f = open(f_each, 'r')
        reader = csv.reader(f, delimiter=" ")
        labellist = []
        for r in reader:
                if int(r[0]) == remove_annotation_number:
                        pass
                else:
                        labellist.append(r)
        print(labellist)
        f.close()
        f = open(f_each,'w')
        for list in labellist:
                f.write(list[0]+" "+list[1]+" "+list[2]+" "+list[3]+" "+list[4]+"\n")
