# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 18:26:41 2018

@author: STU
"""

from wand.image import Image
import glob

file = "c:/movie/*.jpg"      # 불러올 파일 위치
filesave="c:/동서남북"      # 저장 위치
file_list=glob.glob(file)

cn=-1
for t in file_list:
    cn+=1

    oldfilename = file_list[cn]
    row = 2
    col = 2

    with Image(filename = oldfilename) as image:
        height=image.size[1] 
        if height>=500:     # 세로 사이즈가 500 이상일때 처리
            print("old : {0} , {1}".format(image.format , image.size))

            cropHeight = int(image.height/row) #조각별 세로길이
            cropWidth = int(image.width/col)   #조각별 가로길이

            for i in range(0, row): #세로개수 만큼 반복
                for j in range(0, col): #가로개수 만큼 반복
                    left = j*cropWidth
                    right = (j+1)*cropWidth
                    top = i*cropHeight
                    bottom = (i+1)*cropHeight

                    #image[x1:x2, y1:y2] - 가로,세로 범위로 image 자르기
                    with image[left:right, top:bottom] as newimage:
                        print("new : {0} , {1}".format(newimage.format, newimage.size))
                        newimage.save(filename='{0}/{1}_{2}{3}.jpg'.format(filesave,oldfilename[file.rfind('/')+1:-4],i,j)) 
                        # {저장위치}/{파일명}_{상하단}{좌우}.jpg
                    
                    


  
