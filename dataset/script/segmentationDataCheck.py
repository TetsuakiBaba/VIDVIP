# coding: utf-8
import os
import glob
import argparse
import csv
import sys
import math
import pandas as pd
import seaborn as sns
import statistics
import numpy as np
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser(description="Dataset file txt/jpg file checker for VIDVIP sementic segmentation",
                                 usage="> python3 segmentationDataCheck.py -s <path_to_yolo_dataset> -c <path_to_classfile>",
                                 epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str,
                    help="set a jpg/txt search path", required=True)
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)
parser.add_argument("-d", "--duplication",
                    help="duplication check", action="store_true")
parser.add_argument("-b", "--boundingbox",
                    help="count a number of bounding box and analyze", action="store_true")
args = parser.parse_args()


progress = 0

def checkio(data):
    def divide_into_triangles(poly):
        for i in range(len(poly) - 2):
            yield poly[0], poly[i + 1], poly[i + 2]

    def calc_triangle_area(pts):
        (ax, ay), (bx, by), (cx, cy) = pts
        return abs((ax - cx) * (by - ay) - (ax - bx) * (cy - ay)) / 2

    return sum(calc_triangle_area(tri) for tri in divide_into_triangles(data))


# if _ext1 is existed, _ext2 file must be existed.


def fileExistCheck(_ext1, _ext2):
    count = 0
    allfiles = glob.glob(args.search_path+'/**/*'+_ext1, recursive=True)
    print(_ext1+" files: " + str(len(allfiles)))
    for file in allfiles:
        count = count+1
        file_txt = file.replace(_ext1, _ext2)
        # print(file)
        # print(file_txt)

        if os.path.exists(file_txt) == False:
            print("Check Error!!!: "+file_txt+" should be existed.")
    return count


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 0),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


# ここから main処理
flg_duplication = False
if(args.search_path and args.duplication):
    jpg_file_count = fileExistCheck('.jpg', '.txt')
    txt_file_count = fileExistCheck('.txt', '.jpg')
    if(jpg_file_count != txt_file_count):
        print("Error: jpg and txt file correspondance.")
        print("jpg_file_count:"+str(jpg_file_count))
        print("txt_file_count:"+str(txt_file_count))
    else:
        print("Done: jpg-txt correspondance check")
    
    
    array_filename = []
    array_filename_fullpath = []
    allfiles = glob.glob(args.search_path+'/**/*.jpg', recursive=True)
    for file in allfiles:
        array_filename.append(os.path.basename(file))
        array_filename_fullpath.append(file)

    
    for file in allfiles:
        sys.stdout.write("Duplication Check....." +
                         str(progress)+"/"+str(len(array_filename))+"\r")
        progress = progress + 1
        count = 0
        loop_count = 0
        array_duplication = []
        for filename in array_filename:
            if filename == os.path.basename(file):
                count = count + 1
                array_duplication.append(array_filename_fullpath[loop_count])
            loop_count += 1
        if count > 1:
            print("Error:重複したファイル名があります -> " + file + ":")
            print(array_duplication)
            flg_duplication = True
    if flg_duplication == True:
        print("Error: Dupulication filename check")
    else:
        print("Done: Dupublication filename check")

# クラスファイルが指定されていれば，全ファイルのバウンディングボックス数を計算する
if(args.classfile and args.boundingbox):

    # クラスラベルファイルの読み込み
    file_csv_class = open(args.classfile, 'r')
    reader_csv_class = csv.reader(file_csv_class, delimiter=",")
    class_list = []  # クラス名が入った配列
    count_class = []  # 各クラスにbounding box が幾つあるかのカウントを保存
    area = []  # 各クラスの登録領域のそれぞれの面積を保存する
    total_points = [] # 各クラスの登録領域の頂点数合計を保存する
    for class_name in reader_csv_class:
        class_list.append(class_name[0])
        count_class.append(0)
        area.append([])
        total_points.append([])

    print(class_list)
    print(len(class_list))
    print(count_class)
    print(len(count_class))
    number_of_total_file = 0
    number_of_total_points = 0
    allfiles = glob.glob(args.search_path+'/**/*.txt', recursive=True)
    number_of_total_file = len(allfiles)
    for file in allfiles:
        #print(file)
        with open(file) as f:
            txt_reader = csv.reader(f, delimiter=" ")
            for r in txt_reader:
                id = int(r[0])
                pos_list = []
                for p in r:
                    pos_list.append(float(p))
                
                # 最初はclass id なので削除
                pos_list.pop(0)
                pos_area = []
                for i in range(0, len(pos_list)-1, 2):
                    a = [pos_list[i],pos_list[i+1]]
                    pos_area.append(a)
                    
                # print(pos_area)
                segment_area = checkio(pos_area)
                number_of_total_points += len(pos_list)/2
                

                if id < 0 or id > len(class_list)-1:
                    print("Error:" + str(id) + " is out of class range")
                    print(file)
                    exit()
                else:
                    count_class[id] = count_class[id]+1
                    area[id].append(segment_area)  # 面積を計算して保存
                    total_points[id].append(len(pos_list)/2)

    index = 0
    number_of_total_annotation = 0

    f = open("annotations.csv", mode='w')
    print("Number, Name, Count", file=f)
    for c in count_class:
        number_of_total_annotation = number_of_total_annotation + c
        print(str(index) + "," + str(class_list[index])+","+str(c), file=f)
        index = index + 1
    print("Total Number of Points, " + str(number_of_total_points))
    print("Total Annotation,"+str(int(number_of_total_annotation)), file=f)
    print("Total File,"+str(number_of_total_file), file=f)
    print("Total Annotation,"+str(number_of_total_annotation))
    print("Total File,"+str(number_of_total_file))
    print("See detailed annotation number on annotation.csv")

    # Generate a file for bar plot
    # plotting data
    y_data = count_class
    x_labels = class_list
    index = np.arange(len(y_data))  # the x locations for the groups
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots(figsize=(15, 4.0))
    # fig, ax = plt.gcf()

    rects1 = ax.bar(index, y_data, width, label='Our Dataset')
    # ax.set_aspect("equal", adjustable="datalim")
    ax.set_box_aspect(0.2)
    ax.autoscale()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Segmentation')
    ax.set_title('')
    ax.set_xticks(index)
    ax.set_xticklabels(x_labels)
    ax.legend()

    autolabel(rects1, "center")

    fig.tight_layout()
    # plt.grid(True)
    plt.xticks(index, x_labels, rotation='vertical', zorder=0)
    # plt.set_size_inches(18.5, 10.5)
    plt.margins(0.01, 0.1)
    plt.subplots_adjust(bottom=0.40)
    plt.savefig('barplot.png')
    # plt.show()

    # Generate boxplot graph of instance area
    plt.clf()
    plt.boxplot(area, labels=class_list, showfliers=False)
    plt.margins(0.01, 0.1)
    plt.ylabel("Segmentation_Area / Image_Area")
    plt.subplots_adjust(bottom=0.40)
    index = np.arange(1, len(class_list)+1)  # the x locations for the groups
    plt.ylim(0.0, 1.0)
    plt.xticks(index, x_labels, rotation='vertical')
    plt.savefig('boxplot.png')

      # Generate boxplot graph of instance area
    plt.clf()
    plt.boxplot(total_points, labels=class_list, showfliers=False)
    plt.margins(0.01, 0.1)
    plt.ylabel("Segmentation_Area / Image_Area")
    plt.subplots_adjust(bottom=0.40)
    index = np.arange(1, len(class_list)+1)  # the x locations for the groups
    plt.ylim(0.0, 100.0)
    plt.xticks(index, x_labels, rotation='vertical')
    plt.savefig('boxplot_total_points.png')

    # print(len(area))
    # plt.show()
