#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        while True:
            url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year='+str(i)+'&page='+str(j)
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            if soup.select('#old_content > ul > li') == text: # 마지막 페이지 여부확인하면 탈출
                break
            else:
                text = soup.select('#old_content > ul > li')
                #long = len(text) 
                print(str(j)+'번 페이지 영화 제목 저장 시작')
                
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
                    #long -= 1
            j += 1 # 다음 페이지    
            setCsv(i,mdict)


def setCsv(year,mdict):  # mdict -> csv로 파일저장하는 함수
    #global mdict
    a = DataFrame(mdict,index=['year','title','genre','down']).T
    a.to_csv('/home/itwill02/project/data/mdict'+str(year)+'.csv',mode='w',encoding='utf-8') 
    # gpupc : /home/itwill02/project/data

#information(2019,2020)


# information 함수 작동중 멈추면 이어서 받는 함수
def reInformation(year1,year2): # 시작년도, 마지막년도
    for i in range(year1,year2+1): # 년도
        j = 1 # 페이지 수
        text = [] 
        mdict = {}
        while True:
            url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year='+str(i)+'&page='+str(j)
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            if soup.select('#old_content > ul > li') == text: # 마지막 페이지 여부확인하면 탈출
                setCsv1(i,mdict)
                break
            else:
                text = soup.select('#old_content > ul > li')
                
                try: # 중간에 끊어진 년도는 이어서 받기
                    for k in soup.select('#old_content > ul > li'): # j번 페이지에서 각 영화별 페이지글
                        code = re.sub('.[\D]','',k.select_one('a').attrs['href']) # 글번호 추출
                        tmp = pd.read_csv("/home/itwill02/project/data/mdict"+str(i)+".csv")
                        # 처음다운 받는 년도부터는 오류를 발생하면서 except 으로 이동
                        if code not in [str(int(i)) for i in tmp['Unnamed: 0'].values]: # 비교해서 코드 없는 놈부터 시작
                            #print(str(j)+'번 페이지 영화 제목 저장 시작')
                            url1 = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code='+str(code)
                            html1 = urlopen(url1)
                            soup1 = BeautifulSoup(html1,'html.parser')
                            lst = soup1.select('dd > p > span > a') 
                            tup = [] # 장르내용 담을 리스트
                            for s in lst:
                                if s['href'].split('?')[1].split('=')[0] == 'genre': # 장르만 추리기
                                    tup.append(s.text)
                            mdict[code] = [i,k.select_one('a').get_text(),tup,0] # 키 : 글번호, 값 : 년도,영화제목,장르,다운받은여부 값

                except FileNotFoundError:
                    information(i,year2)  # 처음다운 받는 년도들 
                    return
            j += 1
            


def setCsv1(year,mdict):  # mdict -> csv로 파일이어서 추가하는 함수
    #global mdict
    a = DataFrame(mdict,index=None).T
    a.to_csv('/home/itwill02/project/data/mdict'+str(year)+'.csv',mode='a',encoding='utf-8') # 저장경로




# 2nd function
def posterSucker():
    global mdict
    driver = webdriver.Chrome("/home/itwill02/project/chromedriver")
    long = len(mdict.keys())
    # print(str(mdict.values()[0])+'년도 영화 포스터 파일 수집')
    for i in mdict.keys(): # 딕셔너리에서 글번호를 기준으로 반복문
        url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(i) # 포스터 사진 사이트로 이동
        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(1)
        try: # 포스터가 없을때
            alert = driver.switch_to_alert()  # 없다는 팝업 확인
            alert.accept() # 확인 버튼 누름
            mdict[str(i)][2] = 1 # 딕셔너리 다운여부값에 포스터 없음 1로 저장
        except: # 포스터가 있을때
            soup = BeautifulSoup(driver.page_source, 'html.parser') # 소스 가져와서
            with urlopen(soup.find('img',id='targetImage')['src']) as f: # 이미지 테그에서 파일명만 추출
                with open('/home/itwill02/project/data/poster/' + i+'.jpg', 'wb') as w: # 이미지 파일 저장
                    img = f.read() 
                    w.write(img) # 포스터 파일 저장
                    mdict[str(i)][2] = 2 # 딕셔너리 다운여부값에 포스터 있음 2로 저장
                    setCsv()
        long -= 1
        print(str(long)+'개 남음')        
    

# 3rd function
def relayDown():
    global mdict
    a = DataFrame(mdict).T
    relay = a[a[2]==0].index
    driver = webdriver.Chrome("/home/itwill02/project/chromedriver")  # "/home/itwill02/project/chromedriver"
    long = len(relay)
    
    for i in relay:
        url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(i) # 포스터 사진 사이트로 이동
        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(1)
        try: # 포스터가 없을때
            alert = driver.switch_to_alert()  # 없다는 팝업 확인
            alert.accept() # 확인 버튼 누름
            mdict[str(i)][2] = 1 # 딕셔너리 다운여부값에 포스터 없음 1로 저장
        except: # 포스터가 있을때
            soup = BeautifulSoup(driver.page_source, 'html.parser') # 소스 가져와서
            with urlopen(soup.find('img',id='targetImage')['src']) as f: # 이미지 테그에서 파일명만 추출
                with open('/home/itwill02/project/data/poster/' + i+'.jpg', 'wb') as w: # 이미지 파일 저장
                    img = f.read() 
                    w.write(img) # 포스터 파일 저장
                    mdict[str(i)][2] = 2 # 딕셔너리 다운여부값에 포스터 있음 2로 저장
                    setCsv()
        long -= 1
        print(str(long)+'개 남음')

        
if __name__=='__main__':
    information(2010,2017) # 시작년도, 마지막년도
    setCsv() # mdict csv로 저장하는 함수
    posterSucker()
    # relayDown() # posterSucker 작동중 중단되었을 때 이어서 포스터 다운받는 함수

###############################################################################
