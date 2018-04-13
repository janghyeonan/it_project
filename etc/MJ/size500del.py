# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 19:25:00 2018

@author: STU
"""

from PIL import Image
import os
import glob
file = "c:/movie2/*.jpg"          # 폴더 위치
file_list=glob.glob(file)          # 파일 목록 저장

DEL=[]  # 삭제할 사진들 주소 담기
cn=-1
for i in file_list:
    cn+=1
    i = Image.open('{}'.format(i)) #파일 경로 open
    width , height = i.size
    if height<=500:          # 포스터 세로 사이즈 500 이하일때 삭제
        DEL.append(file_list[cn])
        print("삭제되는 영화 포스터 사이즈",width, height)   # 사이즈가 너무 작아 인식을 못할 수 있음

for j in DEL:
    os.remove('{}'.format(j))
    print("이미지가 삭제 되었습니다")  