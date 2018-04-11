#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup # BeautifulSoup 임포트
from selenium import webdriver # 셀레니움 임포트
import re
import time
from urllib.request import urlopen, urlretrieve
from PIL import Image

mdict = {}
def posterSucker(year1,year2):
    driver = webdriver.Chrome("/Users/hbk/data/chromedriver")
    #driver = webdriver.PhantomJS('/Users/hbk/data/phantomjs') # 팬텀 드라이버 경로 선언
    driver.set_page_load_timeout(30)
    global mdict # 이 딕셔너리에 글번호, 영화명 담은 뒤 함수 밖에서도 확인가능하도록 전역변수 선언
    for i in range(year1,year2+1): # 년도
        
        j = 1 # 페이지 수
        text = [] # 
        while True:
            driver.get('https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year='+str(i)+'&page='+str(j))
            driver.implicitly_wait(10)  # 10초 대기
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            if soup.select('#old_content > ul > li') == text: # 마지막 페이지 여부확인하면 탈출
                break
            else:
                text = soup.select('#old_content > ul > li')
                long = len(text) 
                print(str(j)+'번 페이지 영화 제목 저장 시작')
                
                for k in soup.select('#old_content > ul > li'): # j번 페이지에서 각 영화별 페이지글
                    print(str(long)+'개 남음') 
                    code = re.sub('.[\D]','',k.select_one('a').attrs['href']) # 글번호 추출
                    mdict[code] = k.select_one('a').get_text() # 딕션너리 키 : 글번호, 값 : 영화제목 넣음
                    long -= 1
                j += 1 # 다음 페이지

        long2 = len(mdict.keys())
        print(str(i)+'년도 영화 포스터 파일 수집')
        for i in mdict.keys(): # 딕셔너리에서 글번호를 기준으로 반복문
            url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(i) # 포스터 사진 사이트로 이동
            driver.get(url)
            driver.implicitly_wait(5)
            time.sleep(2)
            try: # 포스터가 없을때
                alert = driver.switch_to_alert()  # 없다는 팝업 확인
                alert.accept() # 확인 버튼 누름
                mdict[str(i)] = [mdict[str(i)],'none'] # 딕셔너리에 포스터 없음 none으로 저장
            except: # 포스터가 있을때
                soup = BeautifulSoup(driver.page_source, 'html.parser') # 소스 가져와서
                with urlopen(soup.find('img',id='targetImage')['src']) as f: # 이미지 테그에서 파일명만 추출
                    with open('/Users/hbk/data/poster/' + i+'.jpg', 'wb') as w: # 이미지 파일 저장
                        img = f.read() 
                        w.write(img) # 포스터 파일 저장
                        #im = Image.open('/Users/hbk/data/poster/' + i+'.jpg') #이미지 열기
                        #mdict[str(i)] = [mdict[str(i)],im.size] #이미지 사이즈를 딕션너리에 넣어줌
            long2 -= 1
            print(str(long2)+'개 남음')        
             
    driver.close()
    return mdict
posterSucker(2015,2015)           
        
        
###############################################################################        