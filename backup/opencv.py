#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:28:37 2018

@author: itwill02
"""
import cv2      
import numpy as np
import sys
sys.path
sys.path.append('c:/Users/STU')   #경로추가
img_file ='image2.jpg'   # 이미지지정 
img = cv2.imread(img_file,cv2.IMREAD_GRAYSCALE) #그레이스케일(흑백)
cv2.imwrite('image2_2.jpg',img) #저장
blur = cv2.GaussianBlur(img,(3,3),0)#블러
cv2.imwrite('image2_3.jpg',blur)#저장
canny=cv2.Canny(blur,100,200)#canny()
cv2.imwrite('image2_4.jpg',canny)#저장



# 얼굴인식
cascade_file="/home/itwill02/opencv/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml"
cascade=cv2.CascadeClassifier(cascade_file) 
import os
os.getcwd()
img_name ='abc_1.jpg'
#인식 실행
face=cascade.detectMultiScale(
        img_name,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(50,50))

if len(face)>0:
    print(face)
    color(0,0,225)
    for (x,y,w,h)in face:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), thickness=6)
    #출력
    cv2.imwrite("face2.jpg",image)
else:
    print("아무도 없다!!!!!!!")
    
    
cv2.imshow('누가 인식되었을까?',img)

cv2.waitKey(0)

cv2.destroyAllWindows()