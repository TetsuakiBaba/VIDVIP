import os
import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="create GrayScale Image from vidvips segmentation txt format.",
                                 usage="> python craeteGraySegmentPNGs.py -s <path_to_dataset> -o <path_to_png_output_directory>",
                                 epilog="VIDVIP Project 2023 Tetsuaki BABA")
parser.add_argument("-s", "--search_path", type=str,
                    help="set a jpg/txt search path", required=True)
parser.add_argument("-o", "--output_path", type=str,
                    help="set a output directory to save PNG files", required=True)
args = parser.parse_args()
# ディレクトリ名
input_dir = args.search_path #"all"
output_dir = args.output_path #"allPNG"

# 出力先のディレクトリがなければ作成する
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ディレクトリ内のファイルを取得
for filename in os.listdir(input_dir):
    if filename.endswith(".jpg"):
        # jpgファイルのパスを取得
        img_path = os.path.join(input_dir, filename)
        # 対応するtxtファイルのパスを取得
        txt_path = os.path.join(input_dir, os.path.splitext(filename)[0] + ".txt")
        # pngファイルのパスを作成
        png_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")

        # txtファイルが存在する場合にのみ処理を行う
        if os.path.exists(txt_path):
            # jpg画像を読み込む
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # png画像のための空の配列を作成し、0値で塗りつぶす
            png = np.zeros_like(img)

            # txtファイルを読み込む
            with open(txt_path, "r") as f:
                # 各行を処理する
                for line in f:
                    # ラベル番号と座標を取得
                    label, *coords = map(float, line.strip().split())
                    # 座標を画像サイズに変換して正規化する
                    coords = [(int(x * img.shape[1]), int(y * img.shape[0])) for x, y in zip(coords[::2], coords[1::2])]
                    coords = np.array(coords, dtype=np.int32)
                    coords = np.expand_dims(coords, axis=0)
                    # ラベル番号をグレースケール値に変換
                    color = int(label)+1
                    # 多角形を描画する
                    cv2.fillPoly(png, coords, color)

            # png画像を保存する
            cv2.imwrite(png_path, png)
