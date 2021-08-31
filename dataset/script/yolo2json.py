#coding: utf-8
import os
import glob
import argparse
import csv
import json
from PIL import Image
 
parser = argparse.ArgumentParser(description="VIDVIP YOLO to JSON(CreateML) converter.",
usage = "> python3 yolo2json.py -s <path_to_json_dataset>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)
args = parser.parse_args()

if( args.search_path and args.classfile):
    f_label = open(args.classfile, 'r')
    reader = csv.reader(f_label, delimiter=',')
    classes = []
    for r in reader:
        classes.append(r[0])
    #print(classes)

    file = glob.glob(args.search_path+'/*.txt')
    f_json = open(args.search_path+'/annotations.json','w')
    f_json.write('[\n')
    print(len(file))


    i = 0
    for f_txt in file:
        print(i, len(file))
        # 該当する画像サイズを求める
        filepath_jpg = os.path.splitext(f_txt)[0]+'.jpg'
        image = Image.open(filepath_jpg)
        width,height = image.size
        f_json.write('{"imagefilename":"'+os.path.splitext(os.path.basename(f_txt))[0]+'.jpg","annotations":[')
        f = open(f_txt, 'r')
        print(f_txt)

        length_row = sum([1 for _ in open(f_txt)])
        reader = csv.reader(f, delimiter=" ")
        j = 0
        for r in reader:
            f_json.write('{')
            f_json.write('"label":'+'"'+str(classes[int(r[0])])+'","coordinates":{')
            f_json.write('"x":'+str(int(width*float(r[1])))+',')
            f_json.write('"y":'+str(int(height*float(r[2])))+',')
            f_json.write('"width":'+str(int(width*float(r[3])))+',')
            f_json.write('"height":'+str(int(height*float(r[4]))))
            j += 1
            if j == length_row:
                f_json.write('}}')
            else:
                f_json.write('}},')
        i += 1
        if i == len(file):
            f_json.write(']}\n')
        else:
            f_json.write(']},\n') # 最後のループのときだけカンマは取りたい
    f_json.write('\n]')
    f_json.close()