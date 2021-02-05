import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

import config

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW


# 랜덤 대기시간
def random_wait_time():
    random_wait_min = 3  # 최소 대기시간
    random_wait_max = 8  # 최대 대기시간

    # TODO 공통 라이브러리로 작성  random_wait_time()
    wait_sec = randint(random_wait_min, random_wait_max)
    print("sleep (%d)" % wait_sec)
    return wait_sec


class LikeReflexing():

    def __init__(self):
        super().__init__()
        self.login()
        self.check_accounts_activity()  # 활동 피드의 현황을 반환한다.
        self.Like_reflexing()  # 좋아요 받은 만큼 반사한다.

    def login(self):
        # TODO 공통함수로 작성  login()
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
        popup = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        popup.send_keys(Keys.ENTER)

        time.sleep(2)

        # 알림 설정 팝업 닫기
        try:
            popup = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
            popup.send_keys(Keys.ENTER)
        except:
            pass
        time.sleep(random_wait_time())

    def check_accounts_activity(self):
        # * 활동 피드의 현황을 반환한다.
        # * 예) (하루동안) 신규 활동 총 10개 / 신규 팔로워 10 명 / 좋아요 활동 10개 / 댓글 10개
        # TODO: 새로운 팔로워의 기준이 필요함.
        # 활동 피드 클릭 또는 숨겨진 영역 보이게 하기
        # 활동 피드 버튼 //*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/a
        # 활동 피드 URL https://www.instagram.com/accounts/activity/

        #
        self.browser.get("https://www.instagram.com/accounts/activity/")
        time.sleep(4)
        xpath_active_feed_list = '//div/div[@class="YFq-A"]'
        active_feed_list = self.browser.find_elements_by_xpath(xpath_active_feed_list)

        count_feed_total = len(active_feed_list)
        if not count_feed_total:
            print("no activity in feed.")
            return

        count_liked = 0  # 신규 좋아요/댓글 누른 수
        count_followed = 0  # 신규 팔로워 수
        xpath_new_follower = '//div[@class="PUHRj  H_sJK"]/div[3]/button'  # '팔로우' 버튼
        xpath_new_liked = '//div[@class="PUHRj  H_sJK"]/div[2]/a'  # '이미지' 링크
        new_active_list = {}

        try:
            # '이미지'링크가 존재하면
            actors = self.browser.find_elements_by_xpath(xpath_new_liked)
            for act in actors:
                # 좋아요 카운트 +1
                count_liked += 1
                # 링크 & 계정명 수집
                userName = act.get_attribute('title')
                print("follower liked   ", userName)

                if userName in new_active_list:
                    new_active_list[userName]['count'] = new_active_list[userName]['count'] + 1
                else:
                    new_active_list[userName] = {'count': 1, 'link': act.get_attribute('href')}
        except:
            print("신규 활동 없음")

        try:
            # '팔로우' 버튼이 존재하면
            actors = self.browser.find_elements_by_xpath(xpath_new_follower)
            for act in actors:
                # 팔로워 카운트 +1
                count_followed += 1
                # 링크 & 계정명 수집
        except:
            print("신규 팔로워 없음")

        # 팔로잉, 좋아요 횟수 반환
        print("게시물 좋아요 및 덧글 : ", count_liked, " , 신규 팔로워 ", count_followed)
        print(new_active_list)
        new_active_list = new_active_list
        self.browser.close()
        pass

    def Like_reflexing(self):
        pass
