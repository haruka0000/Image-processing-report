import cv2
import numpy as np
import math
import sys
from scipy import ndimage

# 画像の傾き検出
# @return 水平からの傾き角度
def get_degree(filename_01, filename_02):
    img_1 = cv2.imread(filename_01)
    deg_1 = calc_degree(img_1, filename_01)
    
    img_2 = cv2.imread(filename_02)
    deg_2 = calc_degree(img_2, filename_02)

    deg_dif = deg_2 - deg_1
    print(deg_dif)

    horizontal_img_1 = ndimage.rotate(img_1, deg_1)
    cv2.imwrite('horizontal_' + filename_01, horizontal_img_1)
    horizontal_img_2 = ndimage.rotate(img_2, deg_2)
    cv2.imwrite('horizontal_' + filename_02, horizontal_img_2)
    
    # オリジナル（線が描画されたいない）
    img_1 = cv2.imread(filename_01)
    rotate_img = ndimage.rotate(img_1, -deg_dif)
    cv2.imwrite('hough_rotate.png',rotate_img)

    return deg_dif

def calc_degree(org_img, filename): 
    img = org_img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    negaposi = cv2.bitwise_not(gray)
    # gray = cv2.blur(gray, (5,5))
    edge = cv2.Canny(gray, 50, 110, apertureSize = 3)
    
    minLineLength = 400
    maxLineGap = 5

    # ハフ変換で得られた直線
    lines = cv2.HoughLinesP(edge,1,np.pi/180,125,minLineLength,maxLineGap)
    
    sum_deg = 0;
    count = 0;

    for line in lines:
        for x1,y1,x2,y2 in line:
            # 線分の座標から直線を作成し，角度を算出
            deg = math.degrees(math.atan2((y2-y1), (x2-x1)))
            
            # 直線計算
            # a = (y2 - y1) / (x2 - x1)
            # b = -a * x1 + y1
            # 直線の方程式
            # ax + by = c
            a = y1 - y2
            b = x2 - x1
            c = y1 * x2 - y2 * x1
            start_x = 0
            end_x = img.shape[1]
            if b != 0:
                start_y = int((c - a * start_x) / b)
                end_y = int((c - a * end_x) / b)
            else:
                start_y = img.shape[0]
                end_y = 0
            print(start_y, end_y)
            # 複数の線分から得られた角度の平均用
            sum_deg += deg
            count += 1

            # 利用したラインを描画
            cv2.line(img,(start_x,start_y),(end_x,end_y),(0,0,0),2)

    # 角度の平均
    ave_deg = sum_deg / count 
    cv2.imwrite('houghlines_'+filename,img)

    return ave_deg

if __name__=="__main__":
    filename_01 = sys.argv[1]
    filename_02 = sys.argv[2]
    get_degree(filename_01, filename_02)
    
    