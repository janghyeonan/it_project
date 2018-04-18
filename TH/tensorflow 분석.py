#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:01:25 2018
@author: 김태효
"""

import pandas as pd
from pandas import DataFrame,Series
import numpy as np

# 포스터 색깔, 사물인식 결과, 라벨 데이터
result1 = pd.read_csv('/Users/hbk/github/it_project/TH/total_csv/total_res.csv')
result1.head()

# 포스터 색깔 분석 데이터
result2 = pd.read_csv('/Users/hbk/github/it_project/TH/sample_cv_col_real.csv')
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

y_data = label1.reshape(1105,1)
y_data.shape  # 행 : 1105, 열 : 1


# step.2 : tensorflow로 분석(Softmax Classifier)

import tensorflow as tf

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


===========

# test 예측해 보자
test = pd.read_csv("/Users/hbk/github/it_project/JH/상영예정포스터컬럼파일/youplz.csv")
test1 = test.set_index('id')
test2 = test1.reindex(columns = res3.columns).loc[:,:'zebra'].fillna(0)
test2.values.shape
test2



sess = tf.Session()
pre = sess.run(hypothesis, feed_dict = {X: test2.values})    
print(pre, sess.run(tf.argmax(pre,1)))

test.fillna(0, inplace = True)
test
test1 = test.loc[:,'b1':]
test1.values


