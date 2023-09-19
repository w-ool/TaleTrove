from selenium import webdriver
from bs4 import BeautifulSoup 
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
import random
from selenium.webdriver.common.keys import Keys


nw_url = 'https://comic.naver.com/webtoon?tab=finish'
chromedriver_url = './chromedriver'
driver = webdriver.Chrome(chromedriver_url)
driver.get(nw_url)

sleep(random.uniform(1,1.5))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

id_list = []
name_list = []
story_list = []
genre_list = []
author_list = []
platform_list = []
adult_limited = []

count = 1
id = 0 # index번호 주기 위함
platform = '네이버 웹툰' # 플렛폼 이름

# 진행하다 터질시 이어서 진행할수 있는 코드
# count = 34
# for a in range(count*5):
#     elem = driver.find_element_by_tag_name('body')
#     elem.send_keys(Keys.PAGE_DOWN)
#     sleep(0.5)

for i in range(1812): # 1812 웹툰 횟수
    try:
        # 한번에 출력되는 웹툰이 45개 임으로 45개 크롤링 되면 밑으로 스크롤 내리고 크롤링 45개당 scroll 5번
        if (i+1) % 45 == 0:
            for j in range(count * 5): 
                elem = driver.find_element_by_tag_name('body')
                elem.send_keys(Keys.PAGE_DOWN)
                sleep(0.5)
            count += 1
        
        sleep(random.uniform(1,1.5))
        title = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/div[1]/div[1]/ul/li[{i+1}]/div/a[1]')
        title.click() # 해당 웹툰 클릭하여 단일 웹툰 페이지로 이동

        sleep(random.uniform(1,1.5))

        try:
            # 제목, 줄거리, 장르, 작가 뽑아오기
            name = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/h2').text
            story = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/p').text
            genre = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div').text
            author = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]').text

            name = name.split('\n')[0]
            story = story.replace('\n', ' ')
            genre = genre.replace('\n', ' ')
            author = author.replace('\n', ' / ')
            author = author.split('∙')[0]

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

        except: # 성인 웹툰 클릭되어 로그인 페이지로 이동
            driver.back()

            sleep(random.uniform(1,1.5))

            for j in range(count * 5): # 눌렀던 위치까지 크롤링
                elem = driver.find_element_by_tag_name('body')
                elem.send_keys(Keys.PAGE_DOWN)
                sleep(0.5)

            # 성인 웹툰 이름 크롤링하여 따로 저장
            name = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/div[1]/div[1]/ul/li[{i+1}]/div/a[1]/span/span').text
            adult_limited.append(name)
            print(adult_limited)
        
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
webtoon_data.to_csv('./crawling_data/naver_finished2.csv', encoding='utf-8-sig')

# 성인웹툰 제외된거 따로 출력
adult_data = pd.DataFrame()
adult_data['title'] = adult_limited
adult_data.to_csv('./crawling_data/adult_limited2.csv', encoding='utf-8-sig')