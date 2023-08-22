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

sleep(random.uniform(1,3))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

titles = soup.find_all('li', {'class' : 'DailyListItem__item--LP6_T'})
weekly = soup.find_all('ul', {'class' : 'WeekdayMainView__daily_list--R52q0'})
# print(len(weekly))

id_list = []
name_list = []
story_list = []
genre_list = []
author_list = []
platform_list = []

id = 0
platform = '네이버 웹툰'

login = driver.find_element_by_xpath('/html/body/div[1]/div/header/div[1]/div/div[2]/ul/li[1]/a')
login.click()

input_js = ' \
        document.getElementById("id").value = "{id}"; \
        document.getElementById("pw").value = "{pw}"; \
    '.format(id = "test_id", pw = "test_pw")

sleep(random.uniform(1,3)) 
driver.execute_script(input_js)

sleep(random.uniform(1,3)) 
driver.find_element(By.ID, "log.login").click()

# login_id = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[1]/input')
# login_id.send_keys(id)
# login_password = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[1]/div[2]/input')
# login_password.send_keys(password)
# submit_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/form/ul/li/div/div[7]/button')
# submit_button.click()

for i in range(len(weekly)):
    for j in range(150):
        try:
            sleep(random.uniform(1,3))
            title = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[3]/div[2]/div[{i+1}]/ul/li[{j+1}]/div/a')
            # title = driver.find_element_by_class_name('ContentTitle__title_area--x24vt')
            # /html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/ul/li[1]/div/a
            # /html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/ul/li[2]/div/a
            # /html/body/div[1]/div/div[2]/div[3]/div[2]/div[5]/ul/li[4]/div/a
            title.click()

            sleep(random.uniform(1,3))

            try:
                name = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/h2').text
                story = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/p').text
                genre = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div').text
                author = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]').text

                story = story.replace('\n', ' ')
                genre = genre.replace('\n', ' ')
                author = author.replace('\n', ' / ')
                author = author.split('∙')[0]
                # print(name, story, genre, author)

                if name not in name_list:
                    name_list.append(name)
                    story_list.append(story)
                    genre_list.append(genre)
                    author_list.append(author)
                    id_list.append(id)
                    platform_list.append(platform)

                    id += 1

                driver.back()

            except:
                driver.back()
            
        except:
            break
    

webtoon_data = pd.DataFrame()
webtoon_data['id'] = id_list
webtoon_data['title'] = name_list
webtoon_data['author'] = author_list
webtoon_data['genre'] = genre_list
webtoon_data['story'] = story_list
# webtoon_data.to_csv('naver_unfinished.csv', encoding='utf-8-sig')