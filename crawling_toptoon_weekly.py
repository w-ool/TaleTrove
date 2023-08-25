from selenium import webdriver
from bs4 import BeautifulSoup 
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
import random

id_list = []
name_list = []
story_list = []
genre_list = []
author_list = []
platform_list = []

id = 0 # index번호 주기 위함
platform = '탑툰' # 플렛폼 이름

for j in range(7): # 월~일 별 웹툰 url
    nw_url = f'https://toptoon.com/weekly#weekly{j+1}'
    chromedriver_url = './chromedriver'
    driver = webdriver.Chrome(chromedriver_url)
    driver.get(nw_url)

    sleep(random.uniform(1,1.5))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    for i in range(50):
        try:
            sleep(random.uniform(1,1.5))
            title = driver.find_element_by_xpath(f'/html/body/div[5]/div/div/div/div/ul[{j+1}]/li[{i+1}]/a')
            title.click() # 해당 웹툰 클릭하여 단일 웹툰 페이지로 이동
            sleep(random.uniform(1,1.5))

            try:
                # 제목, 줄거리, 장르, 작가 뽑아오기
                name = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[2]/p/span/span').text
                story = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[5]/p').text
                genre = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[6]').text
                author = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[3]/span[1]').text

                story = story.replace('\n', ' ')
                genre = genre.replace('\n', ' ')

                # 중복된 웹툰은 리스트에 넣지 않음
                if name not in name_list:
                    name_list.append(name)
                    story_list.append(story)
                    genre_list.append(genre)
                    author_list.append(author)
                    id_list.append(id)
                    platform_list.append(platform)

                    id += 1

                driver.back() # 뒷페이지로 이동

            except:
                driver.back()
            
        except:
            break
    
# 데이터 프레임 생성 후 csv파일 만들기
# 반드시 순서가 같아야함 (csv파일 형식 동일하게 하기 위해)
webtoon_data = pd.DataFrame()
webtoon_data['id'] = id_list
webtoon_data['title'] = name_list
webtoon_data['author'] = author_list
webtoon_data['genre'] = genre_list
webtoon_data['story'] = story_list
webtoon_data.to_csv('./crawling_data/toptoon_weekly.csv', encoding='utf-8-sig')