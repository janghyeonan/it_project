#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:16:14 2018

@author: itwill02
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen, urlretrieve
import time
from multiprocessing import Pool

def csv_read_list(year):
    import csv
    import os
    data = csv.reader(open('/home/itwill02/project/test/mdict'+str(year)+'.csv', 'r')) #csv 저장할 폴더 지정
    mnum=[]
    for i in data:
        mnum.append(i)        
    mdict =[mnum[i][0] for i in range(len(mnum))]    
    mdict_s = []    
    for j in (os.listdir('/home/itwill02/project/data/poster1/')): #포스터(이미지 폴더) 가 저장되는 폴더 지정
        mdict_s.append(j.split('.')[0])    
    mn_list =  mdict[1:]
    sf_flist = mdict_s
    for i in sf_flist:
        try:
            mn_list.remove(i)
        except:
            pass
    print(year,'년도 포스터 수', str(len(mdict[1:])))
    print('저장된 파일 수 : ', str(len(sf_flist)))
    print('최종 크롤+포스터 파일 저장해야할 수 :',str(len(mn_list)))
    return mn_list
    
def posterSucker(mn):
    driver = webdriver.PhantomJS("/home/itwill02/project/phantomjs")     #pahntomjs가 있는 폴더 지정
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(mn)
    driver.get(url)
    driver.implicitly_wait(5)    
    time.sleep(1)
    try:
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            with urlopen(soup.find('img',id='targetImage')['src']) as f:
                with open('/home/itwill02/project/data/poster1/' + str(mn)+'.jpg', 'wb') as w: #이미지 파일 저장 폴더 지정
                    img = f.read() 
                    w.write(img)
                    print(str(mn),'-> save complete! 저장되었음!!!!!')
        except:
            print(str(mn),'-> error pass.')
    driver.close()
    driver.quit()
    print(str(mn),'-> phantomjs 종료')


def multi_crawling(st,se,pro): #시작년도, 끝년도, 프로세스개수 
    result = {}
    for i in range(int(st), int(se)):
        start_time = time.time()  
        pool = Pool(processes=int(pro))
        pool.map(posterSucker, csv_read_list(i))    
        print("--- %s seconds ---" % (time.time() - start_time))
        result[i] = (time.time() - start_time)
        print('현재',str(i),'년도가 완료되었습니다.\n 5분 휴식 후 다시 돌아갑니다.')
        time.sleep(300)

if __name__=='__main__':
    multi_crawling(2019,2020,8)

#2010년 
#start_time = time.time()  
#pool = Pool(processes=8)
#pool.map(posterSucker, csv_read_list(2010))
#print("--- %s seconds ---" % (time.time() - start_time))
#--- 322.16980934143066 seconds ---

#2011년
#start_time = time.time()  
#pool = Pool(processes=8)
#pool.map(posterSucker, csv_read_list(2011))
#print("--- %s seconds ---" % (time.time() - start_time))
#--- 1986.5589072704315 seconds ---
    
#{2014: 418.3756973743439,
# 2015: 3598.5499935150146,
# 2016: 3706.6107285022736,
# 2017: 2693.820318222046}

#2013년
#start_time = time.time()  
#pool = Pool(processes=8)
#pool.map(posterSucker, csv_read_list(2013))
#print("--- %s seconds ---" % (time.time() - start_time))
#--- 1986.5589072704315 seconds ---    