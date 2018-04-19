#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup #BeautifulSoup 임포트
from selenium import webdriver #셀레니움 임포트
import re
from urllib.request import urlopen
#from PIL import Image
mdict = {} #데이터를 넣을 딕셔너리 선언
#driver = webdriver.Chrome("/Users/janghyeonan/PythonStudy/chromedriver") #크롬 드라이버 경로 선언
driver = webdriver.PhantomJS('/Users/janghyeonan/PythonStudy/phantomjs') #팬텀js 드라이버 경로 선언
driver.set_page_load_timeout(30)
for a in range(1, 100):    
    driver.get('https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year=2015&page='+str(a)) #네이버 영화 2015년 첫 페이지
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    long = len(soup.select('#old_content > ul > li'))
    print(' 게시글번호 및 영화 제목 저장 시작')
    for i in soup.select('#old_content > ul > li'): #게시판 글 중 제목과 링크의 li선택하기
                         long -= 1
                         mdict[re.sub('.[\D]','',i.select_one('a').attrs['href'])] = i.select_one('a').get_text() #딕션너리에 글번호, 영화제목 넣음.
                         print(str(long)+'개 남음',' 글번호: ',re.sub('.[\D]','',i.select_one('a').attrs['href']), '제목  : ', i.select_one('a').get_text())
                
    long2 = len(mdict.keys())
    print(' 저장된 영화 글번호에 해당하는 포스터 파일 수집')
    
for i in mdict.keys(): #딕셔너리에서 글번호만 뽑아 돌림
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(i) #포스터 사진 사이트로 이동
    driver.get(url)
    driver.implicitly_wait(10)    
    try: #포스터가 없을때
        alert = driver.switch_to_alert()  #없다는 팝업 확인
        alert.accept() #확인 버튼 누름
        mdict[str(i)] = [mdict[str(i)],'none'] #딕셔너리에 포스터 없음 none으로 저장
    except: #포스터가 있을때
        soup = BeautifulSoup(driver.page_source, 'html.parser') #소스 가져와서            
        aa = str(soup.select_one('img#targetImage').attrs['src'])
        if aa[-3:] != 'png':  
            with urlopen(soup.select_one('img#targetImage').attrs['src']) as f: #이미지 테그에서 파일명만 추출                                         
                with open('/Users/janghyeonan/PythonStudy/poster/' + i+'.jpg', 'wb') as w: #이미지 파일 저장
                    img = f.read() 
                    w.write(img) #포스터 파일 저장                    
#                        im = Image.open('/Users/janghyeonan/PythonStudy/poster/' + i+'.jpg') #이미지 열기
                    mdict[str(i)] = [mdict[str(i)],'1'] #이미지 사이즈를 딕션너리에 넣어줌
        elif aa[-3:] =='png':
            print('에이 씨발 성인인증이네')
    long2 -= 1
    print(str(long2)+'개 남음', i + '.jpg')
driver.close() #드라이버 닫기
mdict #결과물확인