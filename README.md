# VIDVIP
VIDVIPは歩道移動時のための日本国内特化型障害物等物体検出データセット開発と学習済みモデルを提供するプロジェクトです．

 * [Project Website](https://tetsuakibaba.jp/project/vidvip/)
 * [データセットREADME](./dataset/README.md)
 * [データセット操作script](https://github.com/TetsuakiBaba/VIDVIP/tree/main/dataset/script)
 * [アプリケーション](./Applications/README.md)

 ## darknetでyolov3 weightsファイルの作成手順メモ
 いつものコマンド

    darknet detector train meta.txt yolo.cfg -gpus 0,1,2,3

 ## CreateMLでmlmodelファイルの作成手順メモ
   1. `coremlフォルダにすべてのjpg, txtファイルをコピー`
   2. `cd script`
   3. `python3 yolo2json.py -s ../coreml`