import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time

import config

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW
TAGS = ['인업같이', '책육아','파이썬', '씨클맞팔']


def random_wait_time():
    random_wait_min = 3  # 최소 대기시간
    random_wait_max = 8  # 최대 대기시간

    wait_sec = randint(random_wait_min, random_wait_max)
    print("sleep (%d)" % wait_sec)
    return wait_sec


class TagFollowering:
    def __init__(self, custom_tag=TAGS[0]):
        print(custom_tag, "태그로 계정을 탐색합니다.")
        self.login()
        self.search_tags(custom_tag)
        self.click_like_recent()

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

    def search_tags(self, custom_tag):
        # 태그 검색 하기
        print("태그 검색 하기")
        search = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search.send_keys(custom_tag)

        time.sleep(2)

        # 최상위 검색 결과로 진입하기 Enter 두번으로 수행
        search.send_keys(Keys.RETURN)  # 최상위 검색결과로 Focus 이동
        search.send_keys(Keys.RETURN)  # 검색결과 새로운 창으로 이동

    def click_like_recent(self):
        # 최근 게시물 선택해서 '좋아요' 클릭
        time.sleep(3)
        feed = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[3]/div[3]/a')
        feed.send_keys(Keys.ENTER)
        self.nextFeed()

        for a in range(10):
            # 좋아요 누르기
            time.sleep(3)
            like_list = self.browser.find_elements_by_xpath('//article//section/span/button')
            like_list[0].click()  # list 중 0번째 버튼을 선택

            # 다음 피드로 이동하기
            self.nextFeed()

        self.browser.quit()

    # 다음 게시물 이동하기 함수
    def nextFeed(self):
        # TODO 함수명 next_feed() 로 변경
        time.sleep(4)
        nextFeed = self.browser.find_element_by_css_selector(
            'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow')
        nextFeed.click()
