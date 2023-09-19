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

titles = soup.find_all('li', {'class' : 'DailyListItem__item--LP6_T'}) # 총 웹툰 수
weekly = soup.find_all('ul', {'class' : 'WeekdayMainView__daily_list--R52q0'}) # 세로 열 수


id_list = []
name_list = []
story_list = []
genre_list = []
author_list = []
platform_list = []

id = 0 # index번호 주기 위함
platform = '네이버 웹툰' # 플렛폼 이름

# 로그인 코드 (일단 사용 x)
#--------------------------------------------------------------------------------------------

# login = driver.find_element_by_xpath('/html/body/div[1]/div/header/div[1]/div/div[2]/ul/li[1]/a')
# login.click()

# input_js = ' \
#         document.getElementById("id").value = "{id}"; \
#         document.getElementById("pw").value = "{pw}"; \
#     '.format(id = "test_id", pw = "test_pw")

# sleep(random.uniform(1,3)) 
# driver.execute_script(input_js)

# sleep(random.uniform(1,3)) 
# driver.find_element(By.ID, "log.login").click()

# login_id = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[1]/input')
# login_id.send_keys(id)
# login_password = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[2]/input')
# login_password.send_keys(password)
# submit_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button')
# submit_button.click()

#----------------------------------------------------------------------------------

for i in range(len(weekly)):
    for j in range(150): # 요일별 횟수 150회(최대 웹툰수보다 많으면 됨) 반복하며 끝에 도달하면 except문으로 break 
        try:
            sleep(random.uniform(1,1.5))
            title = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[3]/div[2]/div[{i+1}]/ul/li[{j+1}]/div/a')
            title.click() # 해당 웹툰 클릭하여 단일 웹툰 페이지로 이동

            sleep(random.uniform(1,1.5))

            try:
                # 제목, 줄거리, 장르, 작가 뽑아오기
                name = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/h2').text
                story = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/p').text
                genre = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div').text
                author = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]').text

                name = name.split('\n')[0] # 휴재인 경우 '휴재' 부분을 지워냄
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
webtoon_data.to_csv('./crawling_data/naver_weekly.csv', encoding='utf-8-sig')