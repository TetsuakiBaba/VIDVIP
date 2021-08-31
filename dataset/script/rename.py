import os
import glob
import argparse
import sys
import random, string

parser = argparse.ArgumentParser(description="指定したディレクトリ以下にあるjpg/txtファイルの名前を指定桁数の乱数名に変更する。名称重複がおきているデータセットに適用する",
                                 usage="> python rename.py -s <path_to_yolo_dataset> -n <number_of_digits>",
                                 epilog="2021 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str,
                    help="set a jpg/txt search path", required=True)
parser.add_argument("-n", "--number_of_digits", type=int,
                    help="set a digits of randmizing", required=True)
args = parser.parse_args()

# def renameWithParentDirName(_files):
#     for f in files:
#         name_parent_directory = os.path.basename(os.path.dirname(os.path.abspath(f)))   
#         filename =  os.path.basename(f)
#         ftitle, text = os.path.splitext(filename)
#         print 'Rename:', filename , 'to', name_parent_directory+'_'+filename
#         os.rename(f, args[1]+'/'+name_parent_directory+'_'+filename)
#     return

# https://qiita.com/Scstechr/items/c3b2eb291f7c5b81902a
def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# jpgでファイルを検索してfilesにすべて格納
files = glob.glob(args.search_path+'/**/*.jpg')

for file in files:
    new_filename = randomname(args.number_of_digits)
    filename = os.path.basename(file)
    parent_directory = os.path.dirname(file)
    
    # jpgファイルを乱数.jpgに変更
    print(file, parent_directory+"/"+new_filename+".jpg")
    os.rename(file, parent_directory+"/"+new_filename+".jpg")

    # txtファイルを乱数.txtに変更
    file_txt, ext = os.path.splitext(filename)
    print(parent_directory+"/"+file_txt+".txt", parent_directory+"/"+new_filename+".txt")
    os.rename(parent_directory+"/"+file_txt+".txt", parent_directory+"/"+new_filename+".txt")