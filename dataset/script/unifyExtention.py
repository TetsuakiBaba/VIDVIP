# coding: utf-8
# 拡張子の表記を統一するスクリプト
# How to use（指定ディレクトリ(path_to_dataset)から .JPGファイルを検索し，.jpgに置き換える）
# python path_to_dataset .JPG .jpg
#
import os
import sys 
import glob

args = sys.argv[1:]
files = (glob.glob(args[0]+'/**/*'+args[1], recursive=True))
extension = args[2]
for f in files:
    ftitle, text = os.path.splitext(f)
    os.rename(f, ftitle+extension)
    print(f+" -> " + ftitle+extension)
