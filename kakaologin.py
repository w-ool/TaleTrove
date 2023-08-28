import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# 다운받은 webdriver의 경로를 지정
service = Service(executable_path='chromedriver.exe')

driver = webdriver.Chrome(service=service)
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
# naver login page로 이동
driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
input_js = ' \
        document.getElementById("id").value = "{id}"; \
        document.getElementById("pw").value = "{pw}"; \
    '.format(id = "test_id", pw = "test_pw")
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
driver.execute_script(input_js)
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
driver.find_element(By.ID, "log.login").click()