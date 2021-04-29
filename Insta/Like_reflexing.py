import re
import time

from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By

from Insta.common.Utils import random_wait_time, login, click_by_xpath, click_element, click_by_css_selector


class LikeReflexing:
    newFollower = "신규 팔로워 : "
    newComments = "최근 댓글 : "
    newLikeAction = "최근 좋아요 : "

    def __init__(self):
        super().__init__()
        login(self)
        new_activity = self.check_accounts_activity()  # 활동 피드의 현황을 반환한다.
        self.Like_reflexing(new_activity)  # 좋아요 받은 만큼 반사한다.

    def check_accounts_activity(self):
        # * 활동 피드의 현황을 반환한다.
        # * 예) (하루동안) 신규 활동 총 10개 / 신규 팔로워 10 명 / 좋아요 활동 10개 / 댓글 10개
        # TODO: 새로운 팔로워의 기준이 필요함.
        new_active_list = {}  # 하룻동안의 좋아요/댓글 활동

        try:
            activity_btn = self.browser.find_element_by_xpath('//a[@class="_0ZPOP kIKUG "]')
        except NoSuchElementException:
            activity_btn = self.browser.find_element_by_xpath('//a[@class="_0ZPOP kIKUG H9zXO"]')

        time.sleep(2)
        click_element(activity_btn)
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
            print("total node counts : ", len(actings))
            for actNum in range(1, len(actings)):
                print(actings[actNum].text)
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
                        self.newFollower += " , @" + userName

                    # 신규 댓글 대응
                    newCommentPattern = re.compile(r'.*댓글')
                    if newCommentPattern.match(userActDescElem[0].text):
                        self.newComments += " , ", actings[actNum].text

                    # 신규 좋아요 구분
                    newLikePattern = re.compile(r'.*좋아')
                    if newLikePattern.match(userActDescElem[0].text):
                        self.newLikeAction += " , @" + userName

                    new_active_list[userName] = {'count': like_count,
                                                 'link': 'https://www.instagram.com/' + userName + '/'}
            print(self.newFollower)
            print(self.newComments)
            print(self.newLikeAction)

        except:
            print("중간에 작업 멈춤.")

        return new_active_list

    def Like_reflexing(self, new_activity):
        isSecretAccount = False
        # 사전에서 하나씩 꺼낸다.
        for userName in new_activity.keys():
            print('Go to ', userName, '\'s page.', 'I got ', new_activity[userName]['count'], ' liked.')

            if new_activity[userName]['count'] == 0:
                break

            # 프로필 페이지로 이동한다.
            self.browser.get(new_activity[userName]['link'])

            try:
                click_by_xpath(self, '//article/div/div/div[1]/div[1]/a')
            except NoSuchElementException:
                print("첫번째 피드 클릭 실패 : 비공개 계정인지 확인 ", new_activity[userName]['link'])
                isSecretAccount = True

            if not isSecretAccount:
                # 좋아요 안눌렸으면 클릭
                for i in range(1, 20):

                    if new_activity[userName]['count'] == 0:
                        break
                    try:
                        # Check label '좋아요'
                        span_button = self.browser.find_element_by_class_name('fr66n')
                        span_ele = span_button.find_element(By.XPATH, './/button/div/span')
                        svg = span_ele.find_element(By.XPATH, './/*[name()="svg"]')
                        # span_button.find_element_by_xpath('//div[@class="_8-yf5 "]/*[name()="svg"][@aria-label="좋아"]')
                        print(svg.get_attribute('aria-label'))
                        if svg.get_attribute('aria-label') == '좋아요':
                            # Heart button click
                            heart_button = self.browser.find_element_by_xpath(
                                '//span[@class="fr66n"]/button[@class="wpO6b  "]')
                            if heart_button:
                                try:
                                    click_element(heart_button)
                                finally:
                                    new_activity[userName]['count'] -= 1
                        else:
                            print('이미 눌렀음')
                    except NoSuchElementException:
                        print("No Element!")
                        pass
                    finally:
                        # 다음피드로 이동
                        self.nextFeed()

    def nextFeed(self):
        next_feed_selector = 'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow'
        click_by_css_selector(self, next_feed_selector)
