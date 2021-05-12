#!/sr/bin/python
# -*- coding: utf-8 -*-
import time

from random import randint
from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

import config

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW

"""
config 의 정보를 토대로 로그인을 시도한다. ↴ ↴
"""


def login(self):
    # 화면띄우기
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("enable-automation")
    self.browser = webdriver.Chrome(config.PATH_TO_WEBDRIVER, chrome_options=options)
    self.browser.get("https://instagram.com")

    # 로딩기다리기
    time.sleep(4)

    # Login ID 속성값 찾고 입력하기
    login_id = self.browser.find_element_by_name('username')
    login_id.send_keys(ID)

    # Login PW 속성값 찾기 입력하기
    login_pw = self.browser.find_element_by_name('password')
    login_pw.send_keys(PW)
    login_pw.send_keys(Keys.RETURN)

    time.sleep(5)

    # 정보저장팝업 닫기
    try:
        popup = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        popup.send_keys(Keys.ENTER)
    except:
        pass
    time.sleep(2)

    # 알림 설정 팝업 닫기
    try:
        popup = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        popup.send_keys(Keys.ENTER)
    except:
        pass
    time.sleep(random_wait_time())


"""
대기시간 (랜덤) 실행 ↴ ↴
"""


def random_wait_time():
    random_wait_min = 3  # 최소 대기시간
    random_wait_max = 8  # 최대 대기시간

    wait_sec = randint(random_wait_min, random_wait_max)
    # print("sleep (%d)" % wait_sec)
    return wait_sec


"""
xpath 를 받아서 클릭한다. ↴ ↴
"""


def click_by_xpath(self, xpath):
    try:
        time.sleep(3)
        selected_ele = self.browser.find_element_by_xpath(xpath)
        selected_ele.click()
    except ElementClickInterceptedException:
        selected_ele.send_keys(Keys.ENTER)
    except NoSuchElementException:
        print("no article in ", xpath)
    finally:
        time.sleep(random_wait_time())


"""
css selector 를 이용해 click! ↴ ↴
"""


def click_by_css_selector(self, selector):
    try:
        selected_ele = self.browser.find_element_by_css_selector(selector)
        selected_ele.click()
        time.sleep(4)
    except ElementClickInterceptedException:
        selected_ele.send_keys(Keys.ENTER)
    except NoSuchElementException:
        print("No Such selector in ", selector)
        pass


""" 
element 를 클릭한다.
클릭 후 로딩을 위해 대기시간을 갖는다. ↴ ↴
"""


def click_element(element):
    try:
        element.click()
    except ElementClickInterceptedException:
        element.send_keys(Keys.ENTER)
    finally:
        time.sleep(random_wait_time())


def has_caution_words(self, desc, userName):
    is_not_a_person = False
    try:
        caution_words = ['오픈톡', '부업문의', '소액투자', '수익금', '재태크', '재택근무']

        for word in caution_words:
            if word in desc:
                filter_result = word, " 문자열 감지했음 ", userName
                print(filter_result)
                return filter_result

    except:
        print('error')

    return
