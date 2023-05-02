import os
import cv2
import json
import glob
import base64
import csv
import argparse

parser = argparse.ArgumentParser(description="VIDVIPS  to Labelme JSON converter.",
usage = "> python vidvipsTxt2LabelmeJson.py -s <path_to_json_dataset> -s <path_to_classfile>",
epilog="2023 Tetsuaki BABA, Motoki MAKI")
parser.add_argument("-s", "--search_path", type=str, help="set a json search path, required=True")
parser.add_argument("-c", "--classfile", type=str,
                    help="set a class file", required=True)

args = parser.parse_args()

def main():
    f_label = open(args.classfile, 'r')
    reader = csv.reader(f_label, delimiter=',')
    labels = []
    for r in reader:
        labels.append(r[0])
    print(labels)

    textfiles = glob.glob(args.search_path+"/*.txt")
    for textfile in textfiles:
        basename = os.path.basename(textfile)
        file_name = os.path.splitext(basename)[0]

        print(file_name)
        image = cv2.imread(args.search_path+"/"+file_name + ".jpg")
        if image is None:
            continue
        height, width, channel = image.shape

        with open(args.search_path+"/"+file_name + ".jpg", "rb") as f:
            img = f.read()
        img_base64 = base64.b64encode(img)

        json_dump = {
            "version" : "5.1.1",
            "flags" : {}
        }
        with open(textfile, "r", encoding="utf-8") as fp:
            shapes = []
            for line in fp:
                textdata = line.split()
                # print(textdata)

                label = labels[int(textdata[0])]
                points = []
                for i in range(int((len(textdata) - 1) / 2)):
                    x = float(textdata[i*2 + 1]) * width
                    y = float(textdata[i*2 + 2]) * height
                    points.append([x, y])

                shape = {
                    "label" : label,
                    "points" : points,
                    "group_id" : None,
                    "shape_type" : "polygon",
                    "flags" : {}
                }
                
                shapes.append(shape)
            json_dump["shapes"] = shapes

        json_dump["imagePath"] = args.search_path + '/'+ file_name + ".jpg"
        json_dump["imageData"] = img_base64.decode("ascii")
        json_dump["imageHeight"] = height
        json_dump["imageWidth"] = width

        # print(json_dump)
        jsonpath = args.search_path + '/' + file_name + '.json'
        jsonfile = open(jsonpath, mode="w")
        json.dump(json_dump, jsonfile, indent=2, ensure_ascii=False)
        jsonfile.close()

    


if __name__ == "__main__":
    main()
