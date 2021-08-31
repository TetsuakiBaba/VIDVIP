# pythonスクリプト使い方一覧
VIDVIP データセットのObject Detectionに関してはYOLO形式で，segmentationに関しては オリジナル形式で作成しています．

## dataCheck.py 
任意のデータセットについて以下の項目をチェックする．指定したディレクトリ以下に含まれる jpg 及び txtが対応しているか，それぞれのインスタンス数( annotation.csv, bargraph.png)及び，各クラスの箱ひげ図(boxplot.png)を自動生成する．生成されたファイルはスクリプトを実行した場所に生成される．具体的な使い方は

```python3 dataCheck.py --help```

にて参照すること．

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
## createTrainValidationList.py
学習させる際に，学習用リストとValidationリストを生成するスクリプト．デフォルトでは全データの9割をtrain，1割をvalidationとして生成します．現在はtrain.txt, validation.txtのみの生成なので，mapの評価を論文で利用するために test.txt も合わせて生成するようにしたほうが良いので今後実装予定．

## renameWithPrentDirName.py
データセットを収集した際にファイル名が他のディレクトリ階層でかぶる可能性がある場合に利用するスクリプトです．例えばデジカメで撮った写真のファイル名そのままで利用していると IMG_0532.JPGみたいなファイル名になりがちですが，これで一斉にデータを収集しちゃうと，連番なんかだともろかぶりしてしまいます．学習させる際には問題は生じませんが，学習環境の都合上，すべての画像ファイルを一つのディレクトリの同じ階層にまとめなければ行けない場合があったりします．こうすると名前被りがおきてしまうため，このスクリプトを利用して親ディレクトリ名をファイル名の頭に一律つけるとよいです．

```python3 renameWithPrentDirName 対象となるDirectory```

## yolo2json.py
macOSの CreateMLで学習を行う場合に利用します．使い方はhelpオプションで確認してください．

## voc2yolo.py
Pascal VOC形式データをYOLOに変換します．使い方はhelpオプションで確認してください．

## coco2yolo.py
coco形式をYOLOに変換します．

## unifyExtention.py
例えば JPGとして保存されてしまった拡張子を一括で jpgにする場合に利用します．
```python3 unifyExtention.py [search_path] .JPG .jpg```
とすることで search_path に含まれる *.JPGファイルを .jpgに変更します．

## showLabelFile.py
指定した番号のアノテーションが含まれているファイルを検索してくれるスクリプト

```python3 [search_path] [search_number]```

## kitti2yolo.py
KITTIデータセットをyolo形式に変換するスクリプト． 使い方・詳細は`--help` で確認してください．

## json2yolo.py
VIDVIPクラウドアノテーション形式（JSON）をyolo形式に変換するスクリプト

## findAndExport.py
指定したクラスラベルが含まれる画像とtxtファイルを指定フォルダにコピーします．特定のアノテーションのみについてチェックを行いたい場合に便利です．詳細は`--help`で．

## fileExtraction.py
アルバイトにアノテーション画像を配布するときに利用するスクリプト．指定したディレクトリにあるjpgファイルのリストから指定した数量のファイルを指定したディレクトリに移動します．



