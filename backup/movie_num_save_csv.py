#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 01:41:20 2018
크롤링 수정본
"""
#수정본 아니잖아
#뭐야 나 작업하는거 뺏어가고 
#태효 해라 그냥 난 잘란다.
#컴퓨터 안꺼지게 잘해라

from bs4 import BeautifulSoup # BeautifulSoup 임포트
from selenium import webdriver # 셀레니움 임포트
import re
import time
from urllib.request import urlopen, urlretrieve
from PIL import Image
from pandas import DataFrame
import pandas as pd
import csv

## 참조사항
# mdict = {code : [year,title,genre,file]} * file : 0(default), 1(poster none), 2(poster ok)
# 1st function : mdict(dict)에 키 : 영화코드번호, 값 : 년도, 영화제목, 장르, 다운받은여부 값 담는 함수
# - csv 저장함수
# - 이어서 받는 함수
# 2nd function : mdict을 입력값으로 받아서 담긴 영화 포스터 다운 받는다
# 3rd function : 2nd에서 오류발생 및 컴퓨터가 뻗어서 정지가 되면 다운받은 포스터에 이어서 받는 함수

mdict = {}

# 1st function
def information(year1,year2):
    
    for i in range(year1,year2+1): # 년도
        j = 1 # 페이지 수
        text = [] 
        mdict = {}
        print(i,'년도')
        while True:
            url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year='+str(i)+'&page='+str(j)
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            if soup.select('#old_content > ul > li') == text: # 마지막 페이지 여부확인하면 탈출
                break
            else:
                text = soup.select('#old_content > ul > li')
                #long = len(text) 
                #print(str(j)+'번 페이지 영화 제목 저장 시작')
                
                for k in soup.select('#old_content > ul > li'): # j번 페이지에서 각 영화별 페이지글
                    #print(str(long)+'개 남음') 
                    code = re.sub('.[\D]','',k.select_one('a').attrs['href']) # 글번호 추출
                    url1 = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code='+str(code)
                    html1 = urlopen(url1)
                    soup1 = BeautifulSoup(html1,'html.parser')
                    lst = soup1.select('dd > p > span > a') 
                    tup = [] # 장르내용 담을 리스트
                    for s in lst:
                        if s['href'].split('?')[1].split('=')[0] == 'genre': # 장르만 추리기
                            tup.append(s.text)
                    mdict[code] = [i,k.select_one('a').get_text(),tup,0] # 키 : 글번호, 값 : 년도,영화제목,장르,다운받은여부 값
                    print(k.select_one('a').get_text())
                    #long -= 1
            j += 1 # 다음 페이지    
            setCsv(i,mdict)


def setCsv(year,mdict):  # mdict -> csv로 파일저장하는 함수
    #global mdict
    a = DataFrame(mdict,index=['year','title','genre','down']).T
    a.to_csv('/Users/janghyeonan/PythonStudy/mdict'+str(year)+'.csv',mode='w',encoding='utf-8') # 저장경로

############
information(2019,2020)


