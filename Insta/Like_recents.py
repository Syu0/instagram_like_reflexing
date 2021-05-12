from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import config
from Insta.common.Utils import login, click_by_xpath, random_wait_time, click_element

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW

from random import randint

CLICK_LIKE_BUTTON_TRY_COUNT = 100  # 좋아요 반사 시도 횟수


class LikeRecents():
    progress_count = 0
    def __init__(self):
        super().__init__()
        print("홈 피드에서 '좋아요'를 누릅니다.")
        login(self)
        self.move_to_home()  # 홈화면으로 이동
        self.click_like_button(CLICK_LIKE_BUTTON_TRY_COUNT)

    def move_to_home(self):
        xpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img'
        click_by_xpath(self, xpath)

    def refresh_and_wait(self):
        time.sleep(random_wait_time())
        print("refresh")
        self.browser.refresh()

    # 좋아요 누르기
    def click_like_button(self, max_try):
        #time.sleep(3)
        pass_this_article = False

        for article_number in range(1, max_try):
            time.sleep(4)

            try:
                # Check label '좋아요'
                span_buttons = self.browser.find_elements_by_class_name('fr66n')
                print("total target count = ", len(span_buttons))

                for span_button_ele in span_buttons:
                    span_ele = span_button_ele.find_element(By.XPATH, './/button/div/span')
                    svg = span_ele.find_element(By.XPATH, './/*[name()="svg"]')
                    if svg.get_attribute('aria-label') == '좋아요':
                        # Heart button click
                        heart_button = span_ele.find_element(By.XPATH, './/../../../*[name()="button"]')
                        if heart_button:
                            try:
                                click_element(heart_button)
                            finally:
                                pass
                    else:
                        print('이미 눌렀음')

                if len(span_buttons) == 0:
                    print("No Empty hearts now.")
                    return

            finally:
                self.progress_count += 1
                self.refresh_and_wait()

        print("좋아요 %d번 시도 종료" % self.progress_count)
        self.browser.quit()
