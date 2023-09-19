from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os
import urllib, requests
import glob
from tqdm import tqdm
from PIL import Image


# 쿼리, chromedriver 실행
title = 'lookism'
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

# 검색창에 query 추가
driver.get('https://www.google.com/search?q=%EC%99%B8%EB%AA%A8%EC%A7%80%EC%83%81%EC%A3%BC%EC%9D%98&tbm=isch&chips=q:%EC%99%B8%EB%AA%A8+%EC%A7%80%EC%83%81%EC%A3%BC%EC%9D%98,g_1:%EC%A2%85%EA%B1%B4:dE4gR84-l4c%3D&rlz=1C1JJTC_koKR1051KR1052&hl=ko&sa=X&ved=2ahUKEwjA3PK12oWBAxWom1YBHY-ZCd4Q4lYoAXoECAEQNg&biw=1519&bih=739')

# 검색 사용시 위에 줄 url 구글 홈 검색창으로 변경하고 아레 코드 활성화
#-------------------------------------------------------------------------
# query = '외모지상주의'
# keyword = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
# keyword.send_keys(query)

# # 검색 실행
# driver.find_element_by_class_name('Tg7LZd').send_keys(Keys.ENTER)

# driver.implicitly_wait(3)
#---------------------------------------------------------------------------

# 스크롤 자동으로 내리며 더보기 버튼 누르기
print('스크롤 내리는중')
elem = driver.find_element_by_tag_name('body')
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
try:
    driver.find_element_by_class_name('mye4qd').send_keys(Keys.ENTER)
    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
except:
    pass

# 이미지 개수 파악

links = []
imgs = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
for img in imgs:
    if img.get_attribute('src') != None :
        links.append(img.get_attribute('src'))
    elif img.get_attribute('data-src') != None :
        links.append(img.get_attribute('data-src'))
    elif img.get_attribute('data-iurl') != None :
        links.append(img.get_attribute('data-iurl'))
        
print('이미지 개수: ', len(links))
time.sleep(1)

# 이미지 다운로드
count = 0   # 이전 마지막 이미지 번호
for i in links:
    start = time.time()
    url = i
    os.makedirs(f'./crawling_img/{title}/', exist_ok=True)
    while True:
        try:
            urllib.request.urlretrieve(url, f'./crawling_img/{title}/{str(count).zfill(4)}_{title}.png')
            print(f'{str(count+1)} / {str(len(links))} / {title} / 다운로드 시간: {str(time.time()-start)[:5]}초')
            break
        except Exception as e:
            print('다운로드 에러')
            time.sleep(5)
        if time.time() - start > 60:
            print('다운로드 패스')
            break
    count += 1
    
print('다운로드 완료')