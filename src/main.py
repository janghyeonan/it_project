#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 16:19:58 2018

@author: itwill02
"""
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import tensorflow as tf
#module 경로 추가 
import sys
sys.path.append('/home/itwill02/project/test/module') 

#mnum_save : 네이버에서 영화번호, 제목, 연도, 장르를 csv로 불러오는 부분 
#img_save  : mnum_save에서 저장한 csv파일을 불러와서 포스터 이미지를 긁어오는 부분 
#img_del : img_save에서 저장한 포스터 이미지 파일 중 이상한 포스터 이미지 파일 제거하는 부분 
#img_text_change : 수집한 이미지 데이터에서 사물인식과 컬러를 뽑아낸 것을 텍스트로 변환한 부분 csv생성
import mnum_save 
import img_save 
import img_del
import img_text_change
import merge_csv

# -------------------------데이터 수집 및 정제 부분 -------------------------

#csv파일 저장 및 이미지 파일 저장 경로 설정
url = '/home/itwill02/project/test/'

#첫째 영화관련정보 수집 후 csv생성 
#mnum_save 메소드 (시작년도, 끝년도, csv파일 저장경로)
#mdict2019.csv, mdict2020.csv 파일이 생성됨.
mnum_save.information(2019,2020, url) 


#둘번째 영화 포스터 이미지 파일 다운로드
#munti_crawling 메소드 (시작년도, 끝년도, 사용할 프로세스 )
#'/poster'폴더에 포스터 이미지 파일이 저장됨.
img_save.multi_crawling(2019,2020,8) 


#세번째 저장한 포스터 정제작업(1. 가로사이즈가 세로사이즈보다 큰 파일 삭제, 2. 사이즈가 너무 작은 파일 삭제)
#'/poster' 폴더 속 정제될 이미지 파일들이 삭제됨.
img_del.small_del(url)
img_del.w_h_cut(url)


#네번째 정제된 포스터 이미지를 데이터화 시킨다. 1. 사물인식, 2. 평균색 
#'/poster' 폴더 속 이미지 파일에게서 데이터를 얻는다.
#
img_text_change.data_text_csv()


#다섯째 네번째에서 얻은 데이터 csv파일과 label이될 csv 파일을 합친다.
merge_csv.total_csv(2010,2010)



# -------------------------예측 부분 -------------------------

# 포스터 색깔, 사물인식 결과, 라벨 데이터
result1 = pd.read_csv('/home/itwill02/project/test/data/total_res.csv')
result1.head()

# 포스터 색깔 분석 데이터
result2 = pd.read_csv('/home/itwill02/project/test/data/total_color_data.csv')
result2.head()

# 인덱스를 영화코드로 재설정
res1 = result1.set_index("Unnamed: 0") 
res2 = result2.set_index("id")

len(res1)
len(res2)

# 조인
res3 = pd.merge(res2,res1,left_index = True, right_index = True)
res3
res3.sum()

## 본격 분석시작

# step.1 : 훈련데이터, 라벨데이터 세팅

train = res3.loc[:,:'zebra'].values  # 라벨컬럼을 제외한 값만 슬라이싱
label = res3['관객수'].values  # 예측해야될 값
label1 = label.astype(int)  # str -> int

# 관객수에 따른 라벨 분류 (0 : 쪽박 ~ 6 : 대박)
label1[label1 <= 100] = 0  # 0 : ~ 100
label1[(label1 > 100) & (label1 <= 100000)] = 1  # 1 : 101 ~ 100000
label1[(label1 > 100000) & (label1 <= 500000)] = 2  # 2 : 100001 ~ 500000
label1[(label1 > 500000) & (label1 <= 1000000)] = 3  # 3 : 500001 ~ 1000000
label1[(label1 > 1000000) & (label1 <= 5000000)] = 4  # 4 : 1000001 ~ 5000000
label1[(label1 > 5000000) & (label1 <= 10000000)] = 5  # 5 : 5000001 ~ 10000000
label1[label1 > 10000000] = 6  # 6 : 10000001 ~

x_data = train
x_data.shape  # 행 : 1105, 열 : 82

y_data = label1.reshape(2400,1)
y_data.shape  # 행 : 1105, 열 : 1

# step.2 : tensorflow로 분석(Softmax Classifier)

X = tf.placeholder(tf.float32, [None,82])  # 열 갯수 82에 맞춤
Y = tf.placeholder(tf.int32, [None, 1])  # 열 갯수 1에 맞춤

Y_one_hot = tf.one_hot(Y, 7)  # 0 ~ 6 : 총 7개
Y_one_hot = tf.reshape(Y_one_hot, [-1, 7]) 


W = tf.Variable(tf.random_normal([82, 7]), name='weight')
b = tf.Variable(tf.random_normal([7]), name='bias')


logits = tf.matmul(X, W) + b
hypothesis = tf.nn.softmax(logits)  # softmax 사용


cost_i = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=Y_one_hot)
cost = tf.reduce_mean(cost_i)

train  = tf.train.GradientDescentOptimizer(learning_rate=0.0001).minimize(cost)  # 학습률 0.0001 설정

prediction = tf.argmax(hypothesis, 1) # 예측결과 확률값이 제일 크면 1 리턴
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1)) # 예측값과 실제값 일치정도
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) # 정확도

###추측해볼 데이터
test = pd.read_csv("/home/itwill02/project/test/data/youplz.csv")
test1 = test.set_index('id')
test2 = test1.reindex(columns = res3.columns).loc[:,:'zebra'].fillna(0)
test2.values.shape
test2

#돌려보자 
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #print(sess.run(Y_one_hot, feed_dict = {Y:y_data}))
    for step in range(100001):
        sess.run(train, feed_dict={X: x_data, Y: y_data})
        if step % 1000 == 0:
            loss, acc = sess.run([cost, accuracy], feed_dict={X: x_data, Y: y_data})
            print("Step: {:5}\tLoss: {:.3f}\tAcc: {:.2%}".format(step, loss, acc))
    
    # 예측 부분         
    pre = sess.run(hypothesis, feed_dict = {X: test2.values}) # test(개봉예정작)
    n = [i for i in range(7) if pre[0][i] == max(pre[0])]
    if n[0] == 0:
        print('\n예상관객수 : 100명 이하')
    elif n[0] == 1:
        print('\n예상관객수 : 100명 초과, 100,000명 이하')
    elif n[0] == 2:
        print('\n예상관객수 : 100,000명 초과, 500,000명 이하')
    elif n[0] == 3:
        print('\n예상관객수 : 500,000명 초과, 1,000,000명 이하')
    elif n[0] == 4:
        print('\n예상관객수 : 1,000,000명 초과, 5,000,000명 이하')
    elif n[0] == 5:
        print('\n예상관객수 : 5,000,000명 초과, 10,000,000명 이하')
    else:
        print('\n예상관객수 : 10,000,000명 초과')