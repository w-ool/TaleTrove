from selenium import webdriver
from bs4 import BeautifulSoup 
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
import random


nw_url = 'https://comic.naver.com/webtoon'
chromedriver_url = './chromedriver'
driver = webdriver.Chrome(chromedriver_url)
driver.get(nw_url)

sleep(random.uniform(1,1.5))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
links = []
weekly = soup.find_all('ul', {'class' : 'WeekdayMainView__daily_list--R52q0'}) # 세로 열 수

for i in range(len(weekly)):
    for j in range(150): # 요일별 횟수 150회(최대 웹툰수보다 많으면 됨) 반복하며 끝에 도달하면 except문으로 break 
        try:
            imgs = driver.find_elements_by_css_selector(f'#container > div.component_wrap.type2 > div.WeekdayMainView__daily_all_wrap--UvRFc > div:nth-child({i+1}) > ul > li:nth-child({j+1}) > a > div > img')
            
            for img in imgs:
                if img.get_attribute('src') != None :
                    links.append(img.get_attribute('src'))
                elif img.get_attribute('data-src') != None :
                    links.append(img.get_attribute('data-src'))
                elif img.get_attribute('data-iurl') != None :
                    links.append(img.get_attribute('data-iurl'))
        

        except:
            break
print('이미지 개수: ', len(links))

