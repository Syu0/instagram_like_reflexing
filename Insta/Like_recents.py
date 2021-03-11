from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time

import config

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW

from random import randint


# 랜덤 대기시간
# TODO 공통함수로 빼기 random_wait_time()
def random_wait_time():
    random_wait_min = 3  # 최소 대기시간
    random_wait_max = 8  # 최대 대기시간

    wait_sec = randint(random_wait_min, random_wait_max)
    print("sleep (%d)" % wait_sec)
    return wait_sec


CLICK_LIKE_BUTTON_TRY_COUNT = 100    # 좋아요 반사 시도 횟수
class LikeRecents():

    def __init__(self):
        super().__init__()
        self.login()
        self.move_to_home()  # 홈화면으로 이동
        self.click_like_button(CLICK_LIKE_BUTTON_TRY_COUNT)

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

    def move_to_home(self):
        xpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img'
        search = self.browser.find_element_by_xpath(xpath)
        try:
            search.click()
        except ElementClickInterceptedException:
            # clkick() 으로 누를 수 없는 버튼은 키보드 ENTER 를 이용한다.
            search.send_keys(Keys.ENTER)
        finally:
            pass

    def refresh_and_wait(self):
        time.sleep(random_wait_time())
        print("refresh")
        self.browser.refresh()

    # 좋아요 누르기
    def click_like_button(self, max_try):
        time.sleep(3)
        pass_this_article = False

        for article_number in range(1, max_try):
            time.sleep(4)

            try:

                # 게시물의 svg 태그의 alri-label이 "좋아요" 인 Node 검색 ( 반대는 좋아요 취소)
                xpath_like_button_svg = '//article//*[@aria-label="좋아요"]/../../../../button[@class="wpO6b "]'
                empty_heart_buttons = self.browser.find_elements_by_xpath(xpath_like_button_svg)

                total_target_count = len(empty_heart_buttons)
                print("total target count = ", total_target_count)

                if total_target_count == 0:
                    print("No Empty hearts now.")
                    self.refresh_and_wait()
                    return

                for target_feed in empty_heart_buttons:

                    # 버튼 클릭 '좋아요'
                    try:
                        target_feed.click()
                        print("clicked")
                    except ElementClickInterceptedException:
                        # clkick() 으로 누를 수 없는 버튼은 키보드 ENTER 를 이용한다.
                        target_feed.send_keys(Keys.ENTER)
                        print("pressed ENTER")
                    finally:
                        time.sleep(random_wait_time())
            except:
                self.refresh_and_wait()

        print("좋아요 %d번 시도 종료" % max_try)
        self.browser.quit()
