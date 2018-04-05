# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 00:20:29 2018

@author: yunsang
"""
#conda install -c conda-forge opencv
import cv2
import numpy as np
def hateerror():
    img_file = 'mal.jpg'
    img = cv2.imread(img_file,cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('mal1.jpg',img)
    cv2.imshow('title',img)
    cv2.waitKey(0) 
    cv2.destroyAllWindow()    
 
hateerror()


blur = cv2.GaussianBlur(mal1,(3,3),0)
    cv2.imwrite('blur.jpg',blur)
    canny=cv2.Canny(blur,100,200)
    cv2.imwrite('canny.jpg',canny)
    cnts,contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
