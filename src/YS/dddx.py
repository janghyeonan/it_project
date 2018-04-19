# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 00:20:29 2018

@author: yunsang
"""
#conda install -c conda-forge opencv
import cv2      
import numpy as np
import sys
sys.path.append('c:/Users/STU')   #경로추가
img_file ='image2.jpg'   # 이미지지정 
img = cv2.imread(img_file,cv2.IMREAD_GRAYSCALE) #그레이스케일(흑백)
cv2.imwrite('image2_2.jpg',img) #저장
blur = cv2.GaussianBlur(img,(3,3),0)#블러
cv2.imwrite('image2_3.jpg',blur)#저장
canny=cv2.Canny(blur,100,200)#canny()
cv2.imwrite('image2_4.jpg',canny)#저장
