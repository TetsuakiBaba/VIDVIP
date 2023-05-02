#coding: utf-8
import os
import glob
import argparse
import csv
 
parser = argparse.ArgumentParser(description="Convert classlist file to voc labelmap",
usage = "> python3 createLabelmap.py -x <path_to_yolo_classlist> ",
epilog="2019 Tetsuaki BABA")
parser.add_argument("-c", "--classfile", type=str, help="set a class file")
args = parser.parse_args()

classlist = []
with open(args.classfile) as f:
    reader = csv.reader(f)
    for row in reader:
        classlist.append(row[0])

print("item { \nname: \"none_of_the_above\"\nlabel: 0\ndisplay_name: \"background\"}")
number = 1
for c in classlist:
    print("item { \nname: \n\""+c+"\"\nlabel:"+str(number)+ "\ndisplay_name: \""+str(number)+"\"\n}")
    number = number + 1