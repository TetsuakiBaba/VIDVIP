#coding: utf-8
import os
import glob
import argparse
import csv
import shutil
 
parser = argparse.ArgumentParser(description="指定したクラスラベルが含まれる画像とtxtファイルを指定フォルダに保存",
usage = "> python3 findAndExport.py -s <path_to_txt_dataset>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str, help="set a txt search path, required=True")
parser.add_argument("-e", "--export_path", type=str, help="set a export path")
parser.add_argument("-n", "--search_number", type=int, help="set a txt search path, required=True")
args = parser.parse_args()

print(args.search_path)
if( args.search_path and args.export_path and args.search_number):
    files = glob.glob(args.search_path+'/**/*.txt', recursive=True)
    for file in files:
        filename_txt = os.path.basename(file)
        filename_jpg, ext = os.path.splitext(filename_txt)
        filename_jpg += '.jpg'
        file_txt = file
        file_jpg, ext = os.path.split(file)
        file_jpg += '/'+filename_jpg
        #print(file_txt, file_jpg)
        with open(file) as f:
            reader = csv.reader(f, delimiter=" ")
            for r in reader:

                # 指定番号が含まれるファイルだったらコピーをする
                if args.search_number == int(r[0]):                    
                    shutil.copy(file_jpg, args.export_path)
                    shutil.copy(file_txt, args.export_path)
                    #shutil.copy()
                    #print(file)
                    break;
                    
else:
    print("error")