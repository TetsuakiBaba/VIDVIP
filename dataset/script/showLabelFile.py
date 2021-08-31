# coding: utf-8
# 指定した番号が path_to_dataset 以下のディレクトリのアノテーションファイルに含まれているものを示す
# How to use
# python3 path_to_dataset label_number
import os
import sys
import csv
import glob

args = sys.argv[1:]
search_id = int(args[1])
files = glob.glob(args[0]+'/**/*.txt', recursive=True)
for f in files:
    f_each = open(f, 'r')
    reader = csv.reader(f_each, delimiter=" ")
    for r in reader:        
        if search_id == int(r[0]):
            print(str(r) + ' in ' + f)
    
