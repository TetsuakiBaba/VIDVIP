#coding: utf-8
import os
import glob
import argparse
import csv
import random
import shutil
 
# 指定したディレクトリにあるjpgファイルのリストから指定した数量のファイルを指定したディレクトリに移動する
parser = argparse.ArgumentParser(description="指定したディレクトリにあるjpgファイルのリストから指定した数量のファイルを指定したディレクトリに移動する",
usage = "> python3 fileExtraction.py -e <path_to_search_directory> -t <path_to_move_directory>",
epilog="2021 Tetsuaki BABA")
parser.add_argument("-e", "--extract_path", type=str, help="抽出するディレクトリを指定")
parser.add_argument("-t", "--to_path", type=str, help="移動するディレクトリ先を指定")
parser.add_argument("-n", "--number_of_extraction", type=int, help="移動させるファイル数を指定")
args = parser.parse_args()

files = glob.glob(args.extract_path+'/**/*.jpg', recursive=True)
random.shuffle(files)
print(str(len(files)) + "個の配列をシャッフルしました")
print(str(args.number_of_extraction) + "個のファイルを" + args.to_path + "に移動します．")
count = 0
for file in files:
    print("move " + file + " to " + args.to_path)
    shutil.move(file, args.to_path)
    count += 1
    if count >= args.number_of_extraction:
        break
#     print(file)