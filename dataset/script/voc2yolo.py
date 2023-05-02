#coding: utf-8
import os
import glob
import argparse
import csv
import json
import xml.etree.ElementTree as ET
 
parser = argparse.ArgumentParser(description="VOC xml to YOLO converter",
usage = "> python3 voc2yolo.py -s <path_to_xml_dataset>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)

args = parser.parse_args()

if( args.search_path and args.classfile ):
    # クラスラベルファイルの読み込み
    file_csv_class = open(args.classfile, 'r')
    reader_csv_class = csv.reader(file_csv_class, delimiter=",")
    class_list = {} # クラス名が入った連想配列をつくろう
    pos = 0
    # クラス名をkeyとしてラベルナンバーを入れておく
    for class_name in reader_csv_class:
        class_list[class_name[0]] = pos
        pos = pos +1
    print(class_list)


    all_xml_files = glob.glob(args.search_path+'/**/*'+'.xml', recursive=True)
    for file in all_xml_files:
        vocdata = ET.parse (file)
        root = vocdata.getroot()

        txt_filename, tmp = os.path.splitext(file)
        txt_filename = txt_filename+".txt"

        print(file)
        # YOLO形式保存用のファイルを同じ名前，拡張子をtxtとして開く
        with open(txt_filename, 'w') as yolo_format_file:
            for child in root:
                if child.tag == 'size':
                    width = int(child.find('width').text)
                    height = int(child.find('height').text)
            for child in root:
                if child.tag == 'object':
                    name = child.find('name').text
                    if class_list.get(name) != None:
                        bounding_box = child.find('bndbox')
                        xmin = int(float(bounding_box.find('xmin').text))
                        ymin = int(float(bounding_box.find('ymin').text))
                        xmax = int(float(bounding_box.find('xmax').text))
                        ymax = int(float(bounding_box.find('ymax').text))
                        print(class_list[name], width, height,  xmin, ymin, xmax, ymax)
                        w = xmax-xmin
                        h = ymax-ymin
                        x_yolo = (xmin + w/2.0)/width
                        y_yolo = (ymin + h/2.0)/height
                        w_yolo = w/width
                        h_yolo = h/height

                        print(str(class_list[name])+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo))
                        #print(txt_filename)
                        yolo_format_file.write(str(class_list[name])+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo)+'\n')
                    else:
                        print("[skipped] No class label: ", name)
            