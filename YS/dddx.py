# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 00:20:29 2018

@author: yunsang
"""
import cv2 
import numpy as np  
 
  
img_color = cv2.imread( 'mal.jpg', cv2.IMREAD_COLOR )  
  
img_gray = cv2.cvtColor( img_color, cv2.COLOR_BGR2GRAY )  
  
cv2.imshow( 'color image', img_color )  
cv2.imshow( 'gray image', img_gray )  
  
cv2.imwrite('result.jpg', img_gray )  
  
cv2.waitKey(0)  
cv2.destroyAllWindow()  

blur = cv2.GaussianBlur(img_gray,(3,3),0)
cv2.imwrite('blur.jpg',blur)
canny=cv2.Canny(blur,100,200)
cv2.imwrite('canny.jpg',canny)
cnts,contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
