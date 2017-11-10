#-*- coding:utf-8 -*-
import cv2
import numpy as np
import os
import glob

# 今やってるのは、画像のサイズが違う
def Vote():

    # カレントディレクトリの絶対パス
    name = os.path.dirname(os.path.abspath(__name__))
    print(name)
    path = os.path.join(name, 'images\\*.jpg')
    print(path)

    jpg_files = [] #jpgリスト
    jpg_files = glob.glob(path)

    """
    for file in jpg_files:
        print(file)
    """

    img_init = cv2.imread(jpg_files[0])

    # ここで2分の1に
    height = int(img_init.shape[0] / 2)
    width = int(img_init.shape[1] / 2)

    #print(height, width)

    """
    for i in range(height):
        for j in range(width):
            print(i, j)
    """

    # リサイズ
    # (height, width)で縦横違ってエラーが出てた
    img_init = cv2.resize(img_init, (width, height))

    #cv2.imshow("img_init", img_init)

    # グレースケール画像に
    img_gray = cv2.cvtColor(img_init, cv2.COLOR_RGB2GRAY)

    # 2値化
    ret, img_gray_thresh = cv2.threshold(img_gray, 70, 255, cv2.THRESH_BINARY_INV)

    # 結果を出力
    cv2.imwrite("img_gray_thresh.jpg", img_gray_thresh)

    #変数用意
    left_white_count = 0
    left_black_count = 0
    right_white_count = 0
    right_black_count = 0

    for i in range(height):
        for j in range(width):
            if (j < width / 2):
                if img_gray_thresh[i][j] == 255:
                    left_white_count+=1 #++は使えない
                else:
                    left_black_count+=1
            else:
                #print(i, j)
                if img_gray_thresh[i][j] == 255:
                    right_white_count+=1
                else:
                    right_black_count+=1

    """
    print("left")
    print("white : " + str(left_white_count) + " black : " + str(left_black_count))

    print("right")
    print("white : " + str(right_white_count) + " black : " + str(right_black_count))
    """

    img_target = cv2.imread(jpg_files[1])

    height2 = int(img_target.shape[0] / 2)
    width2 = int(img_target.shape[1] / 2)

    #print(height, width)

    """
    for i in range(height):
        for j in range(width):
            print(i, j)
    """

    #リサイズ
    img_target = cv2.resize(img_target, (width2, height2))

    #cv2.imshow("img_target", img_target)

    # グレースケール画像に
    img_gray2 = cv2.cvtColor(img_target, cv2.COLOR_RGB2GRAY)

    # 2値化
    ret, img_gray_thresh2 = cv2.threshold(img_gray2, 70, 255, cv2.THRESH_BINARY_INV)

    # 結果を出力
    cv2.imwrite("img_gray_thresh2.jpg", img_gray_thresh2)

    #変数用意
    left_white_count2 = 0
    left_black_count2 = 0
    right_white_count2 = 0
    right_black_count2 = 0

    for i in range(height2):
        for j in range(width2):
            if (j < width2 / 2):
                if img_gray_thresh2[i][j] == 255:
                    left_white_count2+=1 #++は使えない
                else:
                    left_black_count2+=1
            else:
                if img_gray_thresh2[i][j] == 255:
                    right_white_count2+=1
                else:
                    right_black_count2+=1

    """
    print("left2")
    print("white : " + str(left_white_count2) + " black : " + str(left_black_count2))

    print("right2")
    print("white : " + str(right_white_count2) + " black : " + str(right_black_count2))
    """

    # abs()：絶対値
    if (abs(left_white_count - left_white_count2) > abs(right_white_count - right_white_count2)):
        result = "left"
    else:
        result = "right"

    print(result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Vote()
