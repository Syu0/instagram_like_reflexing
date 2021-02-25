import re
import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
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
    # print("sleep (%d)" % wait_sec)
    return wait_sec


class LikeReflexing():
    newFollower = "신규 팔로워 :"
    newComments = "최근 댓글 : "
    def __init__(self):
        super().__init__()
        self.login()
        new_activity = self.check_accounts_activity()  # 활동 피드의 현황을 반환한다.
        self.Like_reflexing(new_activity)  # 좋아요 받은 만큼 반사한다.

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

    def check_accounts_activity(self):
        # * 활동 피드의 현황을 반환한다.
        # * 예) (하루동안) 신규 활동 총 10개 / 신규 팔로워 10 명 / 좋아요 활동 10개 / 댓글 10개
        # TODO: 새로운 팔로워의 기준이 필요함.
        new_active_list = {}  # 하룻동안의 좋아요/댓글 활동

        self.browser.get("https://www.instagram.com/accounts/activity/")
        time.sleep(4)
        xpath_active_feed_list = '//div/div[@class="YFq-A"]'
        active_feed_list = self.browser.find_elements_by_xpath(xpath_active_feed_list)

        count_feed_total = len(active_feed_list)
        if not count_feed_total:
            print("no activity in feed.")
            return new_active_list

        total_acting = 0  # 총 활동 수
        count_followed = 0  # 신규 팔로워 수
        xpath_new_actings = '//div[@class="YFq-A"]/span'  # 새로운 활동

        try:
            actings = self.browser.find_elements_by_xpath(xpath_new_actings)

            for actNum in range(1, len(actings)):
                userNameElem = actings[actNum].find_elements_by_xpath("./a")
                userName = userNameElem[0].text

                userActDescElem = actings[actNum].find_elements_by_xpath("./span")
                # <span>님이 회원님의 게시물을 좋아합니다.</span>
                # <span>님이 회원님을 팔로우하기 시작했습니다.</span>
                # <span>님이 댓글을 남겼습니다</span>
                # print(userName, '', userActDescElem[0].text)

                # 활동유저 카운트 +1
                total_acting += 1

                if userName not in new_active_list:
                    like_count = 3  # 기본으로 좋아요 버튼은 like_count 맡큼 누른다.

                    # 신규 팔로워 구분
                    newFollowerPattern = re.compile(r'.*팔로우')
                    # <span>님이 회원님을 팔로우하기 시작했습니다.</span>
                    if newFollowerPattern.match(userActDescElem[0].text):
                        # print("ㄴ 신규팔로워")
                        like_count = 5
                        count_followed += 1
                        self.newFollower += " , @"+ userName

                    # 신규 댓글 대응
                    newCommentPattern = re.compile(r'.*댓글')
                    if newCommentPattern.match(userActDescElem[0].text):
                        self.newComments += " , @"+ userName
                    new_active_list[userName] = {'count': like_count,
                                                 'link': 'https://www.instagram.com/' + userName + '/'}

            print(self.newFollower)
            print(self.newComments)

        except:
            print("파싱 오류 발")




        return new_active_list

    def Like_reflexing(self, new_activity):

        # 사전에서 하나씩 꺼낸다.
        for userName in new_activity.keys():
            print('Go to ', userName, '\'s page.', 'I got ', new_activity[userName]['count'], ' liked.')

            if new_activity[userName]['count'] == 0:
                break

            # 프로필 페이지로 이동한다.
            self.browser.get(new_activity[userName]['link'])

            time.sleep(3)
            firstItem = self.browser.find_element_by_xpath(
                '//article/div/div/div[1]/div[1]/a')
            time.sleep(3)
            # TODO : 버튼 클릭 공통함수 추가
            # 첫 게시물 클릭
            try:
                firstItem.click()
            except ElementClickInterceptedException:
                firstItem.send_keys(Keys.ENTER)
            finally:
                time.sleep(random_wait_time())

            # 좋아요 안눌렸으면 클릭
            for i in range(1, 20):

                if new_activity[userName]['count'] == 0:
                    break
                try:
                    xpath_like_button_svg = '//article//*[@aria-label="좋아요"]/../../../../button[@class="wpO6b "]'
                    empty_heart_button = self.browser.find_element_by_xpath(xpath_like_button_svg)

                    try:
                        print("clicked")
                        empty_heart_button.click()
                    except ElementClickInterceptedException:
                        empty_heart_button.send_keys(Keys.ENTER)
                    finally:
                        new_activity[userName]['count'] -= 1
                        time.sleep(3)

                except NoSuchElementException:
                    # print("No Element!")
                    pass
                finally:
                    # 다음피드로 이동
                    self.nextFeed()

    def nextFeed(self):
        # print("next feed")
        try:
            nextFeed = self.browser.find_element_by_css_selector(
                'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow')
            nextFeed.click()
            time.sleep(4)
        except NoSuchElementException:
            print("End of feed")
            pass
