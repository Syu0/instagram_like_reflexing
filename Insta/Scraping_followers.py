#!/sr/bin/python
# -*- coding: utf-8 -*-
# (프로세스)
# -> 관심사가 비슷한 계정/ 원하는 지역의 팔로워가 많은 프로필에 찾아간다.
# -> 최근 게시물 1개에 좋아요 누른 계정을 수집힌다
# -> 각각 방문해서 좋아요 여러개와 팔로잉을 한다
# -> 댓글을 남긴다. ex('맞팔해주시면 좋아요는 꾹꾹 잘 눌러드릴 자신이 있어요~!')

import re
import time
from random import randint

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By

import config
from Insta.common.Utils import click_by_xpath, random_wait_time, click_by_css_selector, login, click_element, \
    has_caution_words

ID = config.USER_ID  # 인스타그램 ID realcoders
PW = config.USER_PW  # 인스타그램 PW

BASE_USER = ['inhee_1207', 'lemomente', 'cafe_uncommon']

"""
BASE_USER를 기준으로 팔로워 / 팔로우 유저들을 방문한다.
ㄴ기존의 '좋아요'버튼을 해제 하지 않고, 누를 수 있다.
ㄴ프로필에 필터링 적용.(부업계정 , 비공계 계정 제외)
"""


class ScrapingFollowers:
    targetFollowerList = []  # 팔로워
    targetFollowingList = []  # 팔로우(팔로잉)

    def __init__(self, target_user=BASE_USER[0]):
        for target_user in BASE_USER:
            # self.baseUserName = target_user
            print(target_user, "계정의 팔로워/팔로잉 들을 수집합니다.")
            login(self)

            self.get_followers(target_user)
            self.get_followings(target_user)

            if self.targetFollowerList:
                self.apeal_progress(self.targetFollowerList)

            if self.targetFollowingList:
                self.apeal_progress(self.targetFollowingList)

            self.browser.quit()

    """
    baseUserName 의 프로필에서 팔로워의 리스트를 수집한다. ↴ ↴
    """

    def get_followers(self, baseUserName):
        self.go_to_profile_page(baseUserName)
        time.sleep(10)

        try:

            # 1. '팔로' 리스트 저장
            # click followers list
            follower_button = self.browser.find_elements_by_class_name('Y8-fY')
            alinks = follower_button[1].find_elements(By.CLASS_NAME, '-nal3')
            total_follower_txt = alinks[0].text
            print(total_follower_txt)
            for link in alinks:
                link.send_keys(Keys.RETURN)

            time.sleep(10)

            followers = 0
            follower_element = self.browser.find_elements_by_class_name('jSC57')
            for follower_ul in follower_element:
                followers = follower_ul.find_elements(By.XPATH, './/div/li')

        except ElementNotInteractableException:
            print("비공개 계정", baseUserName)

        # 리스트에 저장
        for user in followers:
            try:
                follow_button = user.find_element(By.XPATH, './/div/div/button')
                # 기존 팔로잉 유저는 거른다.
                if follow_button.text == '팔로우':
                    user_name = user.find_element(By.XPATH, './/div/div/div/div/div/span/a')
                    if user_name.text not in self.targetFollowerList:
                        self.targetFollowerList.append(user_name.text)

            except NoSuchElementException:
                pass

        print('수집결과 ', len(self.targetFollowerList))
        print(self.targetFollowerList)

    """
    프로필에서 '팔로우(팔로잉)' 리스트 저장↴ ↴
    """

    def get_followings(self, baseUserName):
        self.go_to_profile_page(baseUserName)
        time.sleep(10)

        try:

            # 1. '팔로우' 리스트 저장
            # click followers list
            follower_button = self.browser.find_elements_by_class_name('Y8-fY')
            alinks = follower_button[2].find_elements(By.CLASS_NAME, '-nal3')
            total_follower_txt = alinks[0].text
            for link in alinks:
                link.send_keys(Keys.RETURN)

            time.sleep(10)

            followers = 0
            follower_element = self.browser.find_elements_by_class_name('jSC57')
            for follower_ul in follower_element:
                followers = follower_ul.find_elements(By.XPATH, './/div/li')

        except ElementNotInteractableException:
            print("비공개 계정", baseUserName)

        # 리스트에 저장
        for user in followers:
            try:
                follow_button = user.find_element(By.XPATH, './/div/div/button')
                # 기존 팔로잉 유저는 거른다.
                if follow_button.text == '팔로우':
                    user_name = user.find_element(By.XPATH, './/div/div[2]/div[1]/div/div/span/a')
                    if user_name.text not in self.targetFollowingList:
                        self.targetFollowingList.append(user_name.text)

            except NoSuchElementException:
                pass

        print('수집결과 ', len(self.targetFollowingList))
        print(self.targetFollowingList)

    """
    최근 게시물에서 '좋아요' 클릭
    ㄴ 프로필 필터링 기능 추가됨
    """

    def apeal_progress(self, targetUsersList):
        # 리스트에서 한개씩 꺼낸다.
        for userName in targetUsersList:
            isSecretAccount = False
            # 프로필 페이지로 이동한다.
            self.go_to_profile_page(userName)

            random_wait_time()
            try:
                click_by_xpath(self, '//article/div/div/div[1]/div[1]/a')
            except NoSuchElementException:
                print("첫번째 피드 클릭 실패 : 비공개 계정인지 확인 ", userName)
                isSecretAccount = True

            if isSecretAccount:
                break

            profil_area = self.browser.find_element_by_class_name('-vDIg')

            # 필터링 대상이 아니라면 최근 게시물을 클릭한다.
            try:
                if not has_caution_words(self, profil_area.text, userName):
                    self.click_like_recent()

            except NoSuchElementException:
                print("End of feed.")
            pass

            random_wait_time()

    def click_like_recent(self):
        # 최근 게시물 선택해서 '좋아요' 클릭
        time.sleep(3)
        # selected_ele = self.browser.find_element_by_xpath('//article/div/div/div[1]/div[1]/a')
        # click_element(selected_ele)
        # self.nextFeed()

        for a in range(5):
            try:
                # Check label '좋아요'
                ## svg 의 attribute 에 접근하려면 꼭 class_name 으로 검색된 elemente를 사용해야 한다.
                span_button = self.browser.find_element_by_class_name('fr66n')
                span_ele = span_button.find_element(By.XPATH, './/button/div/span')
                svg = span_ele.find_element(By.XPATH, './/*[name()="svg"]')
                if svg.get_attribute('aria-label') == '좋아요':
                    # Heart button click
                    heart_button = self.browser.find_element_by_xpath(
                        '//span[@class="fr66n"]/button[@class="wpO6b  "]')
                    if heart_button:
                        try:
                            click_element(heart_button)
                        finally:
                            pass
                else:
                    print('이미 눌렀음')
            except NoSuchElementException:
                print("No Element!")
                pass
            finally:
                # 다음피드로 이동
                self.nextFeed()

            # 좋아요 누르기
            # time.sleep(3)
            # like_list = self.browser.find_elements_by_xpath('//article//section/span/button')
            # click_element(like_list[0])
            #
            # self.nextFeed()

    def nextFeed(self):
        next_feed_selector = 'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow'
        click_by_css_selector(self, next_feed_selector)

    def go_to_profile_page(self, userName):
        time.sleep(3)
        pageUrl = "https://instagram.com/" + userName + "/"
        self.browser.get(pageUrl)
