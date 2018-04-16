#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 23:48:52 2018

@author: janghyeonan
"""
import requests
from bs4 import BeautifulSoup as bs
import time
from multiprocessing import Pool # Pool import하기
import re
from selenium import webdriver #셀레니움 임포트
llist = []

def get_links(x): 
    req = requests.get('https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year=2014&page=' + x)
    html = req.text
    soup = bs(html, 'html.parser')
    my_titles = soup.select('#old_content > ul > li')
    data = []
    for i in my_titles:
        data.append(re.sub('.[\D]','',i.select_one('a').attrs['href']))
    return data

llist.append(get_links(str(3)))

llist[0]

def gg_content(link):
    driver = webdriver.PhantomJS('/Users/janghyeonan/PythonStudy/phantomjs') #팬텀js 드라이버 경로 선언
    driver.set_page_load_timeout(30)
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(link)
    driver.get(url)
    driver.implicitly_wait(10)    
    try: #포스터가 없을때
        alert = driver.switch_to_alert()  #없다는 팝업 확인
        alert.accept() #확인 버튼 누름
    except: #포스터가 있을때
        soup = bs(driver.page_source, 'html.parser') #소스 가져와서            
        print(str(soup.select_one('img#targetImage')))
    driver.quit() #드라이버 닫기

if __name__=='__main__':
    start_time = time.time()
    pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
    pool.map(gg_content, get_links()) # get_contetn 함수를 넣어줍시다.
    print("--- %s seconds ---" % (time.time() - start_time))
    

