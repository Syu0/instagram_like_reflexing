from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

import config

ID = config.USER_ID #인스타그램 ID realcoders
PW = config.USER_PW #인스타그램 PW

class Instagram():
    def __init__(self):
        super().__init__()
        self.login()

    def login(self):
        #화면띄우기
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars");
        options.add_argument("enable-automation");
        self.browser = webdriver.Chrome(config.PATH_TO_WEBDRIVER, chrome_options=options)
        self.browser.get("https://instagram.com")

        #로딩기다리기
        time.sleep(2)

        # Login ID 속성값 찾고 입력하기
        login_id = self.browser.find_element_by_name('username')
        login_id.send_keys(ID)

        # Login PW 속성값 찾기 입력하기
        login_pw = self.browser.find_element_by_name('password')
        login_pw.send_keys(PW)
        login_pw.send_keys(Keys.RETURN)

        time.sleep(5)

        # 정보저장팝업 닫기
        popup = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        popup.send_keys(Keys.ENTER)

        time.sleep(2)

        # 알림 설정 팝업 닫기
        popup = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        popup.send_keys(Keys.ENTER)

        time.sleep(5)