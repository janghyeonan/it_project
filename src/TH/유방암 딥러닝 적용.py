#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:28:47 2018
@author: 김태효
title : 유방암 데이터에 딥러닝 적용(분류문제)
"""

import pandas as pd
from pandas import Series,DataFrame

data = pd.read_csv("/Users/hbk/Documents/빅데이터 과정/R/wisc_bc_data.csv") # csv파일 불러오기
data.head()

del data['id'] # 분석에 불필요한 부분 삭제
data.head()
len(data.columns) # 31

train = data.drop(['diagnosis'],axis=1).values # 훈련데이타셋 array타입으로 저장
train
len(train[0]) # 30


label = data['diagnosis'].values # 라벨값 (B : 양성, M : 악성)
tmp = label == 'M' # M : True, B : False
label = tmp.astype(int) # 수치화(B->0,M->1)
label.shape = (569,1) # 569행 1열 행렬로 만들어줌(그래야 placeholder 넣을 때 오류 안남)
label


# 위 데이터를 딥러닝으로 분석하기 위해서는 logistic regression을 사용해야 한다

import tensorflow as tf

X = tf.placeholder(tf.float32, [None,30]) # 30 : 데이터 컬럼수에 맞춤
Y = tf.placeholder(tf.float32, [None,1]) # 1 : 라벨 컬럼수에 맞춤

# 은닉층1
W1 = tf.Variable(tf.random_normal([30,50]), name='weight') # 노드 50개
b1 = tf.Variable(tf.random_normal([50]), name='bias')
layer1 = tf.maximum(tf.zeros([50],tf.float32),tf.matmul(X,W1)+b1) # ReLu 함수

# 은닉층2
W2 = tf.Variable(tf.random_normal([50,70]), name='weight') # 노드 70개
b2 = tf.Variable(tf.random_normal([70]), name='bias')
layer2 = tf.sigmoid(tf.matmul(layer1,W2)+b2)

# 은닉층3
W3 = tf.Variable(tf.random_normal([70,50]), name='weight') # 노드 50개
b3 = tf.Variable(tf.random_normal([50]), name='bias')
layer3 = tf.sigmoid(tf.matmul(layer2,W3)+b3)

# 출력층
W4 = tf.Variable(tf.random_normal([50,1]), name='weight')
b4 = tf.Variable(tf.random_normal([1]), name='bias')
output = tf.sigmoid(tf.matmul(layer3,W4)+b4)

cost = -tf.reduce_mean(Y * tf.log(output) + (1 - Y) * tf.log(1 - output))
gradient_descent = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

# 학습시작
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for step in range(5000): # 이유는 모르겠지만 5000번 일때가 결과가 좋게 나온다
        sess.run(gradient_descent, feed_dict = {X:train,Y:label})
        if step % 100 == 0:
            print(step,sess.run(cost, feed_dict = {X:train,Y:label}))
    res = sess.run(tf.round(output), feed_dict = {X:train,Y:label}) # 예측값
    #print('output\n',res)
    per = sum(label == res)/len(label) # 정확도
    print(per)

# 데이터를 전부다 집어넣지 않고 훈련 80, 검증 10, 테스트 10 으로 쪼개서 해바야지
# 함수로 만드면 어떨까하는 생각(아직 고민중)
def deepPoster(train,label): 
    colNum = int(input("컬럼 갯수는? : "))
    hidden = int(input("은닉층 갯수는? : "))
    


================

# 김승혁






