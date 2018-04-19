#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:16:14 2018

@author: itwill02
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen, urlretrieve
import re
import time
from multiprocessing import Pool # Pool import하기

def csv_read_list(year):
    import csv
    import os
    data = csv.reader(open('/Users/janghyeonan/PythonStudy/mdict'+str(year)+'.csv', 'r'))
    mnum=[]
    for i in data:
        mnum.append(i)        
    mdict =[mnum[i][0] for i in range(len(mnum))]    
    mdict_s = []    
    for j in (os.listdir('/Users/janghyeonan/PythonStudy/poster/')):
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
    #return mn_list

def csv_read_list1(year):
    import csv
    import os
    data = csv.reader(open('/Users/janghyeonan/PythonStudy/mdict'+str(year)+'.csv', 'r'))
    mnum=[]
    for i in data:
        mnum.append(i)        
    mdict =[mnum[i][0] for i in range(len(mnum))]    
    mdict_s = []    
    for j in (os.listdir('/Users/janghyeonan/PythonStudy/poster/')):
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
    driver = webdriver.PhantomJS("/Users/janghyeonan/PythonStudy/phantomjs")    
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=174609'
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(mn)
    driver.get(url)
    driver.implicitly_wait(5)    
    #time.sleep(1)
    try:
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            with urlopen(soup.find('img',id='targetImage')['src']) as f:
                with open('/Users/janghyeonan/PythonStudy/poster/' + str(mn)+'.jpg', 'wb') as w:
                    img = f.read() 
                    w.write(img)
                    print(str(mn),'-> save complete! 저장되었음!!!!!')
        except:
            print(str(mn),'-> error pass.')
    driver.close()
    driver.quit()
    print(str(mn),'-> phantomjs 종료')

##############################################################

#파일 이어받기 진행 시 
csv_read_list(2018)
print(csv_read_list1(2018))



#원래 포문
start_time1 = time.time()  
for i in csv_read_list1(2018)[0:15]:
    posterSucker(i)
print("--- %s seconds ---" % (time.time() - start_time1))



#멀티프로세싱
start_time = time.time()  
pool = Pool(processes=8)
pool.map(posterSucker, csv_read_list1(2018)[51:90])
print("--- %s seconds ---" % (time.time() - start_time))

##############################################################















#2010꺼 완료 
start_time = time.time()  
pool = Pool(processes=8)
pool.map(posterSucker, csv_read_list(2010))
print("--- %s seconds ---" % (time.time() - start_time))
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
    
result = {}
for i in range(2014, 2018):
    start_time = time.time()  
    pool = Pool(processes=8)
    pool.map(posterSucker, csv_read_list(i))    
    print("--- %s seconds ---" % (time.time() - start_time))
    result[i] = (time.time() - start_time)
    print('현재',str(i),'년도가 완료되었습니다.\n 5분 휴식 후 다시 돌아갑니다.')
    time.sleep(300)
    

#2013년
start_time = time.time()  
pool = Pool(processes=8)
pool.map(posterSucker, csv_read_list(2013))
print("--- %s seconds ---" % (time.time() - start_time))
#--- 1986.5589072704315 seconds ---

import csv
year = '2017'
data = csv.reader(open('/home/itwill02/project/data/mdict'+year+'.csv', 'r'))
mnum=[]
for i in data:
    mnum.append(i) 
len(mnum)    
#7280+8625+10083+10815+10843+10109+10447+7589
#
#75791 * 2
#151582/60    
#2526/60    
#30+40+60+60+60+60+60+40
#410/60
#    
    
    
2-2
    