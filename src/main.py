#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:15:44 2018

@author: janghyeonan
"""

#1. 크롤링
#네이버에서 분류한 1)영화 번호, 2)영화 이름, 3)장르, 4)개봉연도
#csv로 저장

#2. 1번 데이터에서 영화 포스터 이미지 파일 저장
# 1번에서 얻어진 csv파일의 영화번호를 모아서 파일 다운로드
# 중간에 멈출것을 대비하여, 1번에서 얻어진 영화번호와 실제로 저장된 영화 이미지 파일 명과 비교 후 나머지만 이어서 저장하기 기능
# 포스터 이미지 파일이 많기 때문에 따로 실행, 


#3. 2번 완료 후 포스터 이미지 파일 정제
# 파일 형식이 달라 4,5번 진행이 어려운 포스터 삭제 진행
# 포스터 사이즈가 아닌 가로 길이가 세로길이 보다 긴 파일 삭제
# 사물인식이 잘 되지 않는 사이즈가 작은 파일 삭제


#4. object detection을 이용한 컬럼 데이터 추출
# object detection은 사전에 학습된 모델을 사용하는 것임.
# 파일 수만큼 사물인식을 시켜서, 인식되는 값을 csv파일에 저장

#5. 구글 devision을 이용한 컬러 데이터 추출
#구글 devision를 이용하여 데이터 컬럼을 추가함


#6 1,2번에서 크롤링 되지 않은 데이터 즉 라벨이 될 데이터 (관객수, 매출)의 데이터를
#수집하여 따로 저장


#7. 학습데이터, 라벨 데이터를 한군데에 저장

#8. 모델에 적용, 결과 도출


#####################
import cv2
import time
from sklearn.cluster import KMeans
import pandas as pd
from pandas import Series, DataFrame
import time

def image_color_cluster(file_name):
    image = cv2.imread(file_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clt = KMeans(n_clusters=2)
    clt.fit(image)
    ccc = []
    for center in clt.cluster_centers_:
        ccc.append(center)
    return ccc

def img_play(file_name):
    df = DataFrame()
    start_time = time.time()
    file_name =(file_name)
    a = image_color_cluster(file_name)
    print('===== 컬러 추출시간%s초 걸림======' % (int(time.time() - start_time)))
    rgb_dict = {}
    rgb_dict['id'] = file_name.split('/')[4].split('.')[0]
    rgb_dict['r1'] = int(a[0][0])
    rgb_dict['g1'] = int(a[0][1])
    rgb_dict['b1'] = int(a[0][2])
    rgb_dict['r2'] = int(a[1][0])
    rgb_dict['g2'] = int(a[1][1])
    rgb_dict['b2'] = int(a[1][2])    
    b = DataFrame(Series(rgb_dict)).T
    b = b.set_index('id')
    df = df.append(b)    
    return df


###########상영 예정작##########
ffile = '/Users/janghyeonan/PythonStudy/youplz.jpg'
data = object_detection_go(ffile) ## 사물인식
data2 =  img_play(ffile)          ## 이미지 컬러 추출 RGB 2개 값
##############################
ndata = DataFrame(Series(data['item'])).T
ndata.index = data2.index
total_data = data2.merge(ndata, left_index=True, right_index = True)
print(total_data)
total_data.to_csv('/Users/janghyeonan/PythonStudy/youplz.csv', mode="w", encoding="utf-8")



