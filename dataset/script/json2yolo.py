#coding: utf-8
import os
import glob
import argparse
import csv
import json
 
parser = argparse.ArgumentParser(description="iSee Json to YOLO converter",
usage = "> python3 json2yolo.py -s <path_to_json_dataset>",
epilog="2019 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")

args = parser.parse_args()

if( args.search_path ):
    all_json_files = glob.glob(args.search_path+'/**/*'+'.json', recursive=True)
    for file in all_json_files:
        json_open = open(file, 'r')
        json_load = json.load(json_open)
        img_filename = json_load['fileName']        
        img_width = json_load['size']['width']
        img_height = json_load['size']['height']
        txt_filename, tmp = os.path.splitext(file)
        txt_filename = txt_filename+".txt"
        print(img_filename)
        print(img_width)
        print(img_height)
        objects = json_load['objects']
        with open(txt_filename, 'w') as yolo_format_file:
            for object in objects:
                id = object['labelNumber']
                xmin = object['boudingBox']['xmin']
                xmax = object['boudingBox']['xmax']
                ymin = object['boudingBox']['ymin']
                ymax = object['boudingBox']['ymax']
                w    = (xmax-xmin)
                h    = (ymax-ymin)
                x_yolo = (xmin + w/2.0)/img_width
                y_yolo = (ymin + h/2.0)/img_height
                w_yolo = w/img_width
                h_yolo = h/img_height
                print(str(id)+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo))
                print(txt_filename)
                yolo_format_file.write(str(id)+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo)+'\n')
            

            