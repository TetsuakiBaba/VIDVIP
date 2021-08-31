#coding: utf-8
import os
import glob
import argparse
import csv
from PIL import Image
from pathlib import Path

def parentpath(path='.', f=0):
    return Path(path).resolve().parents[f]



parser = argparse.ArgumentParser(description="COCO's YOLO(txt) to VIDVIP YOLO(txt) converter.",
usage = "> python3 coco2yolo.py -s <path_to_json_dataset> -c <path_to_class_label>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)
args = parser.parse_args()

if( args.search_path and args.classfile):
    # クラスラベルファイルの読み込み
    file_csv_class = open(args.classfile, 'r')
    reader_csv_class = csv.reader(file_csv_class, delimiter=",")
    class_list = []
    pos = 0
    # クラス名をkeyとしてラベルナンバーを入れておく
    for class_name in reader_csv_class:
        class_list.append(class_name[0])
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
                    id = int(r[0])                    
                    x_yolo = float(r[1])
                    y_yolo = float(r[2])
                    w_yolo = float(r[3])
                    h_yolo = float(r[4])
                    
                    id_yolo = -1
                    if id == 0 :
                        id_yolo = 0
                    elif id == 1:
                        id_yolo = 1
                    elif id == 2:
                        id_yolo = 2
                    elif id == 3:
                        id_yolo = 3
                    elif id == 5:
                        id_yolo = 4
                    elif id == 6:
                        id_yolo = 5
                    elif id == 7:
                        id_yolo = 6
                    elif id == 8:
                        id_yolo = 7
                    elif id == 9:
                        id_yolo = 8
                    else:
                        id_yolo = -1
                    if id >= 0 and id <= 8:
                        print(id, x_yolo, y_yolo, w_yolo, h_yolo)
                        yolo_format_file.write(str(id)+" "+ str(x_yolo) + " " + str(y_yolo)+" "+str(w_yolo)+" "+str(h_yolo)+'\n')
                   
        

