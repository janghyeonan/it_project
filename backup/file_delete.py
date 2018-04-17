#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 01:21:01 2018

@author: itwill02
"""

from PIL import Image
import os
import glob
file = "/home/itwill02/project/data/poster/*.jpg"          # 폴더 위치
file_list=glob.glob(file)          # 파일 목록 저장
len(file_list)

DEL=[]  # 삭제할 사진들 주소 담기
cn=-1
for i in file_list:
    cn+=1
    i = Image.open('{}'.format(i)) #파일 경로 open
    width,height = i.size
    if height<=500:          # 포스터 세로 사이즈 500 이하일때 삭제
        DEL.append(file_list[cn])
        print(file_list[cn],': ',width, height)   # 사이즈가 너무 작아 인식을 못할 수 있음


for j in DEL:
    print(j, "이미지가 삭제 되었습니다")
    os.remove('{}'.format(j))
    
#cannot identify image file '/home/itwill02/project/data/poster/116066~7~8.jpg'
#/home/itwill02/project/data/poster/117311.jpg
#/home/itwill02/project/data/poster/83893.jpg    
   
    
############
145802_00
im = open('/home/itwill02/project/data/poster_4cut/145802_00.jpg')
print(im.size)
im.show()
#########

#문제는 다른 exif라는 포멧방식이 문제다. 
from PIL import Image
import os
import glob

file = "/home/itwill02/project/data/poster/*.jpg"          # 폴더 위치
file_list=glob.glob(file)          # 파일 목록 저장

DEL=[]  # 삭제할 사진들 주소 담기
cn=-1
for i in file_list:
    cn+=1
    print(cn,']',i)
    i = Image.open('{}'.format(i)) #파일 경로 open
    width , height = i.size    
    if width > height:
        DEL.append(file_list[cn])
        print(file_list[cn],': ',width, height)   # 가로가 더 큰것들은 영화 포스터가 아님

for j in DEL:
    print(j, "이미지가 삭제 되었습니다")
    os.remove('{}'.format(j))    
    
    
    

