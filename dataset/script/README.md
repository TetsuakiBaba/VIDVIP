# pythonスクリプト使い方一覧
VIDVIP データセットのObject Detectionに関してはYOLO形式で，segmentationに関しては オリジナル形式（YOLO形式拡張）で作成しています．これら形式の管理運用に利用しているpythonスクリプトがいくつか種類があるので、このページに記述します。なおVIDVIPのObejct Detectionをvidvipo、Segmentationをvidvipsとして表記しています。

# vidvipo専用
## dataCheck.py 
任意のデータセットについて以下の項目をチェックする．指定したディレクトリ以下に含まれる jpg 及び txtが対応しているか，それぞれのインスタンス数( annotation.csv, bargraph.png)及び，各クラスの箱ひげ図(boxplot.png)を自動生成する．生成されたファイルはスクリプトを実行した場所に生成される．具体的な使い方は

```python3 dataCheck.py --help```

にて参照すること．

## kitti2yolo.py
KITTIデータセットをyolo形式に変換するスクリプト． 使い方・詳細は`--help` で確認してください．

## json2yolo.py
VIDVIPクラウドアノテーション形式（JSON）をyolo形式に変換するスクリプト

## yolo2json.py
macOSの CreateMLで学習を行う場合に利用します．使い方はhelpオプションで確認してください．

## voc2yolo.py
Pascal VOC形式データをYOLOに変換します．使い方はhelpオプションで確認してください．

## coco2yolo.py
coco形式をYOLOに変換します．


# 共通
vidvipo, vidvipsのどちらのデータセットでも活用可能なスクリプトの紹介
## remapLabel.py
```python3 remapLabel.py -s [検索対象となるデータセットディレクトリ] -c [remapfile]```

ラベルマップファイル(remapfile)に従って，指定したパス以下にあるアノテーションファイル（.txt）のラベル番号を一括変更します．ラベル変換マップの書式は変換対象番号と，変換先番号をスペースで区切ったssv（space separated value）形式．例えば以下の形式の場合はラベル番号3,4を入れ替えてる変換マップファイルです．
```
0 0
1 1
2 2
3 4
4 3
```
## createTrainValidationTest.py
学習させる際に，学習用リストとValidationリストを生成するスクリプト．
デフォルト設定は、データセットの15%をランダムにValidationデータ（validation.txt）として、
データセットの3%をランダムにTestデータとして（test.txt）として、残りの82%をランダムにtrainデータセット（train.txt）としてリストを作成する なおDeeplabによるSegmentationではtest.txtは現状利用していないが、3%くらいなので気にしない。

## renameWithPrentDirName.py
データセットを収集した際にファイル名が他のディレクトリ階層でかぶる可能性がある場合に利用するスクリプトです．例えばデジカメで撮った写真のファイル名そのままで利用していると IMG_0532.JPGみたいなファイル名になりがちですが，これで一斉にデータを収集しちゃうと，連番なんかだともろかぶりしてしまいます．学習させる際には問題は生じませんが，学習環境の都合上，すべての画像ファイルを一つのディレクトリの同じ階層にまとめなければ行けない場合があったりします．こうすると名前被りがおきてしまうため，このスクリプトを利用して親ディレクトリ名をファイル名の頭に一律つけるとよいです．

```python3 renameWithPrentDirName 対象となるDirectory```


## unifyExtention.py
例えば JPGとして保存されてしまった拡張子を一括で jpgにする場合に利用します．
```python3 unifyExtention.py [search_path] .JPG .jpg```
とすることで search_path に含まれる *.JPGファイルを .jpgに変更します．

## showLabelFile.py
指定した番号のアノテーションが含まれているファイルを検索してくれるスクリプト

```python3 [search_path] [search_number]```


## findAndExport.py
指定したクラスラベルが含まれる画像とtxtファイルを指定フォルダにコピーします．特定のアノテーションのみについてチェックを行いたい場合に便利です．詳細は`--help`で．

## fileExtraction.py
アルバイトにアノテーション画像を配布するときに利用するスクリプト．指定したディレクトリにあるjpgファイルのリストから指定した数量のファイルを指定したディレクトリに移動します．

# Segmentation (vidvips)
セグメンテーション専用のスクリプト。2023年3月16日時点ではdeeplabv3を対象としたデータセットを作成したのち、tensorflowで学習させている。

## segmentationDataCheck.py
object detectionで利用している dataCheck.py のセグメンテーション版。基本的には使い方は同じで、ファイル名の重複チェックやデータセットの統計データや箱ひげ図を生成してくれる。

```python segmentationDataCheck.py --help```

にて詳細を確認。

## createGraySegmentPNGs.py
deeplabで学習するために必要な領域分割されたグレースケールpngを生成するためのpython スクリプト。手っ取り早く学習に進める場合はこちらを利用してください。一旦labelme形式にするスクリプトも用意していますが、どちらかというとこちらはデータセットの確認用途で使うとよいでしょう。本スクリプトの利用方法は
```python createGraySegmentPNGs.py -h```
を参照すること。

## vidvipsTxt2labelmeJson.py
vidvips形式のアノテーションファイルをlabelme形式のjsonファイルに一括変換するスクリプト。学習に必要な領域分割画像を生成するために利用します。本スクリプトはCSIの慎さんが記述したものに馬場が修正したファイルです。最初にjpgおよびtxtファイルを同じディレクトリに全てコピーした後に本スクリプトを利用してください。例えば all というディレクトリに学習用のjpg及びtxtをコピーした後、以下のように実行するとallディレクトリに同名のjsonファイルが生成されます。

```python vidvipsTxt2LabelmeJson.py -s ./test -c names_c41_segmentation.txt```

## labelme2voc.py
このファイルはvidvipプロジェクトで作成したものではなく、labelmeプロジェクトで作成されたものをここにpythonスクリプトだけ便宜上おいています。このスクリプトはlabelmeファイル階層に保存された学習データをvoc形式に変換するスクリプトです。labelmeファイル階層例は以下の通り。

```
labelmeDir
├── all
│   ├── 001.jpg
│   ├── 001.json
│   ├── 002.jpg
│   └── 002.json
└── labels.txt # 先頭に __ignore__, _background_ を含む
```

これに対して、vocのファイル階層形式は以下の通り。

```
任意のディレクトリ名/
　├ JPEGImages # 撮影されたjpg画像
　├ SegmentationClass # npy形式データ
　├ SegmentationClassPNG # 領域分割されたpng画像
　├ SegmentationClassVisualization # 領域分割+ラベル名表示も含まれた画像
　└ class_names.txt # ラベル一覧（一番最初に_background_が追加されている）
```

labelmeDirを含むディレクトリをrootDirとした場合、以下のコマンドを実行すると

```python labelme2voc.py "./rootDir/labelmeDir/all" "./rootDir/vidvip" --labels ./rootDir/labelmeDir/labels.txt```

引数は順番 [input_dir] [output_dir]となっている。
生成されるファイル階層は次のようになる。tfrecordの生成にはvidvipディレクトリを利用する。

```
rootDir
├── labelmeDir
│   ├── all
│   │   ├── 001.jpg
│   │   ├── 001.json
│   │   ├── 002.jpg
│   │   └── 002.json
│   └── labels.txt
└── vidvips # labelme2voc.pyで自動生成されるディレクトリ
    ├── JPEGImages
    │   ├── 001.jpg
    │   └── 002.jpg
    ├── SegmentationClass
    │   ├── 001.npy
    │   └── 002.npy
    ├── SegmentationClassPNG
    │   ├── 001.png
    │   └── 002.png
    ├── SegmentationClassVisualization
    │   ├── 001.jpg
    │   └── 002.jpg
    └── class_names.txt
```