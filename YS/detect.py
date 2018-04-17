# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 23:17:42 2018

@author: yunsang
"""

import cv2      
import numpy as np
import sys
sys.path.append('c:/Users/STU')   #경로추가
img_file ='mal1.jpg'   # 이미지지정
img =cv2.imread(img_file,cv2.IMREAD_COLOR)
cv2.imwrite('image2_1.jpg',img)          
img=cv2.resize(img, None, fx=0.6, fy=0.63, interpolation=cv2.INTER_AREA)
img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )   #그레이스케일(흑백)
cv2.imwrite('image2_2.jpg',img) #저장
blur = cv2.GaussianBlur(img,(3,3),0)#블러
cv2.imwrite('image2_3.jpg',blur)#저장
canny=cv2.Canny(blur,100,200)#canny(윤곽)
cv2.imwrite('image2_4.jpg',canny)#저장
cnts,contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x,y,w,h=cv2.boundingRect(cnt)
    if h<20:continue
    red=(0,0,150)
    cv2.rectangle(img,(x,y),(x+w,y+h),red,2)

box1=[]
f_count=0
select=0
plate_width=0

for i in range(len(contours)):
    cnt=contours[i]          
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area=w*h  #area size
    aspect_ratio = float(w)/h # ratio = width/height
    if (aspect_ratio>=0.2)and(aspect_ratio<=1.0)and(rect_area>=100)and(rect_area<=700): 
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        box1.append(cv2.boundingRect(cnt))
         
for i in range(len(box1)): ##Buble Sort on python
    for j in range(len(box1)-(i+1)):
        if box1[j][0]>box1[j+1][0]:
            temp=box1[j]
            box1[j]=box1[j+1]
            box1[j+1]=temp
                         
         #to find number plate measureing length between rectangles
for m in range(len(box1)):
    count=0
    for n in range(m+1,(len(box1)-1)):
        delta_x=abs(box1[n+1][0]-box1[m][0])
        if delta_x > 150:
            break
            delta_y =abs(box1[n+1][1]-box1[m][1])
            if delta_x ==0:
                delta_x=1
                if delta_y ==0:
                    delta_y=1           
                    gradient =float(delta_y) /float(delta_x)
                    if gradient<0.25:
                        count=count+1
               #measure number plate size         
                        if count > f_count:
                            select = m
                            f_count = count;
                            plate_width=delta_x
          
            
cv2.imwrite('snake.jpg',img)
          
          
number_plate=img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]+10:180+box1[select][0]] 
#영역 사이즈조절 
resize_plate=cv2.resize(number_plate,None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR) 
#리사이징
plate_gray=cv2.cvtColor(resize_plate,cv2.COLOR_BGR2GRAY)
#그레이스케일
ret,th_plate = cv2.threshold(plate_gray,150,255,cv2.THRESH_BINARY)
          
cv2.imwrite('plate_th.jpg',th_plate)
kernel = np.ones((3,3),np.uint8)
er_plate = cv2.erode(th_plate,kernel,iterations=1)
er_invplate = er_plate
cv2.imwrite('er_plate.jpg',er_invplate)

#테서렉트로 이미지 글자를 실제 텍스트로 변환 (ocr) 미완성 
#설치후 테스트 
recogtest=Recognition()
result=recogtest.ExtractNumber()
print(result)







# 얼굴인식
sys.path.append('c:/Users/yunsang/Anaconda3/Lib/site-packages/cv2/data')
cascade_file="haarcascade_frontalface_default.xml"
cascade=cv2.CascadeClassifier(cascade_file) 
#인식 실행
 
face=cascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(50,50))     #############코드는 맞으나 에러 (다시 확인 )




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


