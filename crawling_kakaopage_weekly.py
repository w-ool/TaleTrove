from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import random
import time
from selenium.webdriver.common.keys import Keys

id_list = []
name_list = []
story_list = []
genre_list = []
author_list = []
platform_list = []

id = 0
platform = '카카오페이지 웹툰'

for i in range(7):
    try:
        kw_url = f'https://page.kakao.com/menu/10010/screen/52?tab_uid={i+1}'
        chromedriver_url = './chromedriver.exe'
        driver = webdriver.Chrome(service=Service(chromedriver_url))
        driver.get(kw_url)
        sleep(random.uniform(1, 1.5))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.find_all('div', {
            'class': 'absolute top-0 left-0 h-full w-full rounded-8pxr border-[0.5px] border-solid border-sp-thumb-line'})
        # # /html/body/div[1]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/a/div/div[4]
        # weekly = soup.find_all('div', {'class' : 'px-11pxr'})
        # /html/body/div[1]/div/div[2]/div/div[2]/div[1]/div/div[4]

        for j in range(300):
            try:
                # 수정된 부분-----------------------------------------------
                sleep(random.uniform(1, 1.5))

                if (j + 1) % 25 == 0:
                    banner = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/div/img')
                    action = webdriver.ActionChains(driver)
                    action.move_to_element(banner).perform()
                    sleep(random.uniform(2, 3))
                    print('wait')

                try:
                    title = driver.find_element_by_xpath(
                        f'/html/body/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[{j + 1}]/div/a')
                    # /html/body/div[1]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/a 스크롤 내리기 전 xpath
                    # /html/body/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/a 스크롤 다 내린 후 변경된 xpath
                    print(title)
                    title.click()
                except:
                    for a in range(1):
                        elem = driver.find_element_by_tag_name('body')
                        elem.send_keys(Keys.PAGE_UP)
                        sleep(1)
                    title = driver.find_element_by_xpath(
                        f'/html/body/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[{j + 1}]/div/a')
                    # /html/body/div[1]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/a 스크롤 내리기 전 xpath
                    # /html/body/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/a 스크롤 다 내린 후 변경된 xpath
                    print(title)
                    title.click()
                # -----------------------------------------------------------------
                sleep(random.uniform(1, 1.5))

                try:
                    # 제목, 줄거리, 장르, 작가명
                    name = driver.find_element_by_xpath(
                        f'/html/body/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[3]/div[2]/span').text
                    # / html / body / div[1] / div / div[2] / div[1] / div[1] / div[1] / div[1] / div / div[3] / div[2] / span
                    story_see = driver.find_element_by_xpath(
                        f'/html/body/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/a/div')
                    story_see.click()  # 웹툰 작품소개 페이지 이동
                    sleep(random.uniform(1, 1.5))
                    num = 3

                    try:
                        story = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[3]/span').text
                    # / html / body / div[1] / div / div[2] / div[1] / div[2] / div[2] / div[3] / span
                    # / html / body / div[1] / div / div[2] / div[1] / div[2] / div[2] / div[1] / span
                    except:
                        story = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]/span').text
                    genre = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[1]/span[4]').text
                    # / html / body / div[1] / div / div[2] / div[1] / div[1] / div[1] / div[1] / div / div[3] / div[2] / div[1] / div[1] / span[4]
                    author = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[2]/div/span').text
                    # / html / body / div[1] / div / div[2] / div[1] / div[1] / div[1] / div[1] / div / div[3] / div[2] / div[1] / div[2] / div / span
                    story = story.replace('\n', '')
                    story = story.split('※')[0]
                    story = story.split('[로고 및 표지 디자인]')[0]
                    story = story.split('[표지 및 타이틀 로고 디자인]')[0]
                    story = story.split('ⓒ')[0]
                    genre = genre.replace('\n', ' ')
                    author = author.replace('\n', ' / ')
                    author = author.split('∙')[0]
                    print(name, story, genre, author)

                    # 중복된 웹툰은 리스트에 넣지 않음

                    if name not in name_list:
                        name_list.append(name)
                        story_list.append(story)
                        genre_list.append(genre)
                        author_list.append(author)
                        id_list.append(id)
                        platform_list.append(platform)
                        id += 1

                    driver.back()
                    sleep(random.uniform(1, 1.5))
                    driver.back()

                except:
                    driver.back()

            except:
                break

    except:
        break

webtoon_data = pd.DataFrame()
webtoon_data['id'] = id_list
webtoon_data['title'] = name_list
webtoon_data['author'] = author_list
webtoon_data['genre'] = genre_list
webtoon_data['story'] = story_list
webtoon_data.to_csv('./crawling_data/kakaopage_weekly.csv', encoding='utf-8-sig')