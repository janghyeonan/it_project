#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 02:07:46 2018
@author: 김태효
"""

import pandas as pd
from pandas import DataFrame,Series
import numpy as np

od_d = pd.read_csv('/Users/hbk/github/it_project/JH/od_d.csv')
data = od_d.fillna(0)
data1 = data.drop('Unnamed: 0',axis=1)
data1.sum()

data2 = data1.set_index('id')
data2.shape


dict = {}
for i in range(2010,2018):
    tmp = pd.read_csv('/Users/hbk/github/it_project/TH/total_csv/'+str(i)+'.csv')
    dict[i] = tmp[['code','관객수','매출액']]
    
type(dict[2010])

total = DataFrame(columns = ['code','관객수','매출액'])

for i in range(2010,2018):
    total = total.append(dict[i])

total.shape
total_data = total.set_index('code')
total_data

result = data2.merge(total_data,left_index=True,right_index=True) # 2378,78

result.to_csv('/Users/hbk/github/it_project/TH/total_csv/total_res.csv',mode='w',encoding='utf-8')

#total['code'].to_csv('/Users/hbk/github/it_project/TH/total_csv/code.csv',mode='w',encoding='utf-8')


## 본격 분석시작
lst = sorted(result['관객수'],reverse=True)
# 0 : ~ 100
# 1 : 101 ~ 100000
# 2 : 100001 ~ 500000
# 3 : 500001 ~ 1000000
# 4 : 1000001 ~ 5000000
# 5 : 5000001 ~ 10000000
# 6 : 10000001 ~

import scipy.stats as sp
sp.stats.describe(lst)
lst.describe()

x = result['관객수']

np.percentile(x, 0)  # 0
np.percentile(x, 25) # 295
np.percentile(x, 50) # 11796.5
np.percentile(x, 75) # 259883
np.percentile(x, 100) # 17613682


#### 

train = result.loc[:,:'zebra'].values
label = result['관객수'].values
label1 = label.astype(int)  # str -> int

label1[label1 <= 100] = 0  # 0 : ~ 100
label1[(label1 > 100) & (label1 <= 100000)] = 1  # 1 : 101 ~ 100000
label1[(label1 > 100000) & (label1 <= 500000)] = 2  # 2 : 100001 ~ 500000
label1[(label1 > 500000) & (label1 <= 1000000)] = 3  # 3 : 500001 ~ 1000000
label1[(label1 > 1000000) & (label1 <= 5000000)] = 4  # 4 : 1000001 ~ 5000000
label1[(label1 > 5000000) & (label1 <= 10000000)] = 5  # 5 : 5000001 ~ 10000000
label1[label1 > 10000000] = 6  # 6 : 10000001 ~


x_data = train
x_data.shape # 2378,76
y_data = label1.reshape(2378,1)


import tensorflow as tf

X = tf.placeholder(tf.float32, [None,76]) 
Y = tf.placeholder(tf.int32, [None, 1])

Y_one_hot = tf.one_hot(Y, 7)  # 0 ~ 6 : 총 7개
Y_one_hot = tf.reshape(Y_one_hot, [-1, 7]) 


W = tf.Variable(tf.random_normal([76, 7]), name='weight')
b = tf.Variable(tf.random_normal([7]), name='bias')


logits = tf.matmul(X, W) + b
hypothesis = tf.nn.softmax(logits)

## cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis)))
cost_i = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=Y_one_hot) # 위랑 같은 기능의 메소드
cost = tf.reduce_mean(cost_i) # 확률적인 부분이라서 평균으로 생각해야 한다

train  = tf.train.GradientDescentOptimizer(learning_rate=0.0001).minimize(cost)

prediction = tf.argmax(hypothesis, 1) # 예측결과 확률값이 제일 크면 1 리턴
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1)) # 일치율
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(10000):
        sess.run(train, feed_dict={X: x_data, Y: y_data})
        if step % 1000 == 0:
            loss, acc = sess.run([cost, accuracy], feed_dict={X: x_data, Y: y_data})
            print("Step: {:5}\tLoss: {:.3f}\tAcc: {:.2%}".format(step, loss, acc))







#####

train.shape # (2378, 76)
label = label.reshape(2378,1)
label.shape

train.dtype
label.dtype
label = label.astype(int)

train
for i in label:
    if i <= 100:
        i

import tensorflow as tf

X = tf.placeholder(tf.float64, [None,76])
Y = tf.placeholder(tf.float64, [None,1])

W = tf.Variable(tf.random_normal([76,1],dtype=tf.float64,seed=0),name='weight')
b = tf.Variable(tf.random_normal([1],dtype=tf.float64,seed=0),name='bias')
hypothesis = tf.matmul(X,W) + b

cost = tf.reduce_mean(tf.square(Y-hypothesis))
gradient_descent = tf.train.GradientDescentOptimizer(learning_rate = 0.01).minimize(cost)
# gradient_descent = tf.train.AdamOptimizer(learning_rate=0.05).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(5000):
        sess.run(gradient_descent, feed_dict={X:train,Y:label})
        cost_val = sess.run(cost, feed_dict={X:train,Y:label})
        if step % 100 == 0:
            print(step,cost_val)
    res = sess.run(hypothesis,feed_dict={X:train})
    print(res)


