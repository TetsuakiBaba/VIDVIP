#coding: utf-8
import os
import glob
import argparse
import csv
from PIL import Image
from pathlib import Path

def parentpath(path='.', f=0):
    return Path(path).resolve().parents[f]



parser = argparse.ArgumentParser(description="VIDVIP KITTI(txt) to YOLO(txt) converter.",
usage = "> python3 kitti2yolo.py -s <path_to_json_dataset> -c <path_to_class_label>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)
args = parser.parse_args()

if( args.search_path and args.classfile):
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

    files = glob.glob(args.search_path+'/*.txt')

    for file in files:
        print(file)
         # YOLO形式保存用のファイルを同じ名前，拡張子をtxtとして開く
        path_parent = parentpath(file,0)
        filename_txt = str(path_parent)+'/yolo/'+os.path.basename(file)
        print(filename_txt)
        
        with open(filename_txt, 'w') as yolo_format_file:
            with open(file) as f:
                txt_reader = csv.reader(f, delimiter=" ")
                
                print(txt_reader)
                for r in txt_reader:                       
                    name = r[0]
                    minx = float(r[4])
                    miny = float(r[5])
                    maxx = float(r[6])
                    maxy = float(r[7])
                    
                    # 画像サイズは一定
                    img_width = 1242
                    img_height = 375
                    
                    w = (maxx-minx)
                    h = (maxy-miny)
                    x_yolo = (minx + w/2)/img_width
                    y_yolo = (miny + h/2)/img_height
                    w_yolo = w/img_width
                    h_yolo = h/img_height
                    name_yolo = ''
                    if name == 'Car' or name == 'Van':
                        name_yolo = 'car'
                    elif name == 'Pedestrian' or name == 'Person_sitting':
                        name_yolo = 'person'
                    elif name == 'Cyclist':
                        name_yolo = 'bicycler'
                    elif name == 'Tram':
                        name_yolo = 'bus'
                    else:
                        name = 'out_of_range'

                    if name != 'out_of_range':
                        print(name_yolo, x_yolo, y_yolo, w_yolo, h_yolo)
                        yolo_format_file.write(str(class_list[name_yolo])+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo)+'\n')
                   
        

