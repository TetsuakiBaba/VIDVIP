# coding: utf-8
import os
import glob
import argparse
import csv
import sys
import random

parser = argparse.ArgumentParser(description="Create train.txt, validation.txt and test.txt for YOLO",
                                 usage="> python3 createTrainValidationTest.py -s <path_to_yolo_dataset>",
                                 epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str,
                    help="set a jpg/txt search path")
args = parser.parse_args()

count = 0
count_train_files = 0
count_test_files = 0
count_validation_files = 0
# データセットの15%をランダムにValidationデータとしてリストを作成する validation.txt
# データセットの3%をランダムにTestデータとしてリストを作成する test.txt
if(args.search_path):
    allfiles = glob.glob(args.search_path+'/**/*.jpg', recursive=True)
    print("Total Files: "+str(len(allfiles)))
    file_train = open('train.txt', 'w')
    file_test = open('test.txt', 'w')
    file_validation = open('validation.txt', 'w')
    for file in allfiles:
        random_number = random.random();
        if random_number < 0.03:
            count = count+1
            count_test_files += 1
            # print(file)
            file_test.write(file+'\n')
        elif random_number < 0.15:
            count = count + 1
            count_validation_files += 1
            file_validation.write(file+'\n')
        else:
            count_train_files += 1
            file_train.write(file+'\n')
    # print(count)
    file_train.close()
    file_test.close()
    file_validation.close()

    print("Success: " + str(count_train_files) +
          " for training, "+ str(count_validation_files) + " for validation, " + str(count_test_files)+" for testing")

else:
    print("Please set search PATH. for more information use --help option")
