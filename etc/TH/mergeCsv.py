#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:59:24 2018
@author: 김태효
"""
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re

def total_csv(year1,year2):
    for i in range(year1,year2+1):
        
        data = pd.read_csv("/Users/hbk/github/it_project/WK/"+str(i)+".csv")
        data = data[['영화명','관객수','매출액','개봉일']]
        
        data['영화명'][data['영화명'].isna()] = ''
        data['관객수'][data['관객수'].isna()] = ''
        data['매출액'][data['매출액'].isna()] = ''
        data['개봉일'][data['개봉일'].isna()] = ''

        data.columns = ['title','관객수','매출액','개봉일']
            
            
        tmp1 = []
        tmp2 = []
        tmp3 = []
        tmp4 = []
        for j in data.values:
            tmp1.append(re.sub(' ','',j[0]))
            tmp2.append(re.sub(',','',j[1]))
            tmp3.append(re.sub(',','',j[2]))
            tmp4.append(j[3].split('.')[0])
        data['title'] = Series(tmp1).values
        data['관객수'] = Series(tmp2).values
        data['매출액'] = Series(tmp3).values
        data['개봉일'] = Series(tmp4).values
        
        
        data_0 = data[data['개봉일']==str(i)]
        del data_0['개봉일']
        
        
        data1 = pd.read_csv("/Users/hbk/github/it_project/TH/mdict_csv/mdict"+str(i)+".csv")
        data1.columns = ['code','year','title','genre','down']
        
        
        lst1 = []
        for k in data1['title']:
            #print(re.sub(' ','',i.split(' (')[0]))
            lst1.append(re.sub(' ','',k.split(' (')[0]))
        data1['title'] = Series(lst1).values
        
        
        a = pd.merge(data_0,data1)
        
        a1 = a.set_index('code')
        a1.to_csv('/Users/hbk/github/it_project/TH/total_csv/'+str(i)+'.csv',mode='w',encoding='utf-8')
        
        
total_csv(2011,2017)
