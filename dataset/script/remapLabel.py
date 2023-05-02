# coding: utf-8
import os
import glob
import argparse
import csv
import sys
import math

parser = argparse.ArgumentParser(description="YOLO形式のクラスラベルをマップに基づいて再割り当てします．",
                                 usage="> python3 remapLabel.py -s <path_to_yolo_dataset> -c <path_to_class_remap_file>",
                                 epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str,
                    help="set a jpg/txt search path", required=True)
parser.add_argument("-c", "--class_remap_file", type=str,
                    help="set a remap class file", required=True)
args = parser.parse_args()

remap = {}
if args.search_path and args.class_remap_file:
    f_csv = open(args.class_remap_file, 'r')
    reader = csv.reader(f_csv, delimiter=" ")
    for r in reader:
        remap[int(r[0])] = int(r[1])
    print("created remap array")
    print(remap)
    f_csv.close()
    files = glob.glob(args.search_path+'/**/*.txt', recursive=True)
    for file in files:
        f_csv = open(file, 'r')
        reader = csv.reader(f_csv, delimiter=" ")
        labellist = []
        for r in reader:
            if remap[int(r[0])] == -1:
                print("Error: undefined instance number")
                print(r)
                print("exit()")
                exit()
            r[0] = str(remap[int(r[0])])
            
            labellist.append(r)
        # 無事に該当ファイルすべての登録情報を取得できたら
        # print(labellist)
        f_csv.close()
        f_csv = open(file,'w')
        for list in labellist:
            f_csv.write(list[0]+" "+list[1]+" "+list[2]+" "+list[3]+" "+list[4]+"\n")
        f_csv.close()
