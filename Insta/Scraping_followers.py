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

BASE_USER = ['cafe_uncommon']


class ScrapingFollowers:
    baseUserName = ''
    targetUsersList = []

    def __init__(self, target_user=BASE_USER[0]):
        for target_user in BASE_USER:
            self.baseUserName = target_user
            print(target_user, "계정의 팔로워들을 방문합니다.")
            login(self)
            self.targetUsersList = self.get_target_users(self.baseUserName)

            self.apeal_progress()

            self.browser.quit()

    def go_to_profile_page(self, userName):
        time.sleep(3)
        pageUrl = "https://instagram.com/" + userName + "/"
        self.browser.get(pageUrl)

    def get_target_users(self, baseUserName):
        self.go_to_profile_page(baseUserName)
        time.sleep(10)
        targetUsersList = []

        try:

            # 1. '팔로워' 리스트 저장
            # click followers list
            follower_button = self.browser.find_elements_by_class_name('Y8-fY')
            alinks = follower_button[2].find_elements(By.CLASS_NAME, '-nal3')
            total_follower_txt = alinks[0].text
            print(total_follower_txt)
            for link in alinks:
                link.send_keys(Keys.RETURN)
            print('총 팔로우 : ', total_follower_txt, '명')

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
                    if user_name.text not in targetUsersList:
                        targetUsersList.append(user_name.text)

            except NoSuchElementException:
                pass

        # TODO : 2. '팔로우' 리스트 저장

        # click followers list
        # 팔로워 창 닫기 클릭
        # close_buttons = self.browser.find_elements_by_class_name('wpO6b')
        # close_buttons[1].click()
        #
        # alinks = self.browser.find_elements_by_class_name('-nal3')
        # total_follow_txt = alinks[2].text
        # print (total_follow_txt)
        # alinks[2].send_keys(Keys.RETURN)
        #
        # print('총 팔로우 : ', total_follow_txt, '명')
        #
        # time.sleep(10)
        #
        # followers = 0
        # follower_element = self.browser.find_elements_by_class_name('jSC57')
        # for follower_ul in follower_element:
        #     followers = follower_ul.find_elements(By.XPATH, './/div/li')
        #
        # time.sleep(10)
        # # 리스트에 저장
        # for user in followers:
        #     follow_button = user.find_element(By.XPATH, './/div/div/button')
        #     # 기존 팔로잉 유저는 거른다.
        #     if follow_button.text == '팔로우':
        #         user_name = user.find_element(By.XPATH, './/div/div/div/div/div/span/a')
        #         if user_name.text not in targetUsersList:
        #             targetUsersList.append(user_name.text)

        # 스크롤하기
        # get users
        # time.sleep(3)
        # user_names_xpath = '//a[@class="FPmhX notranslate MBL3Z"]'
        # user_name_tags = self.browser.find_element_by_xpath(user_names_xpath)
        # lpos = len(user_name_tags)
        # touchAction = TouchActions(self.browser)
        # touchAction.scroll_from_element(user_name_tags[lpos], 20)

        # return list

        print('수집결과 ', len(targetUsersList))
        print(targetUsersList)
        return targetUsersList

    def apeal_progress(self):
        # 리스트에서 한개씩 꺼낸다.
        for userName in self.targetUsersList:
            # 좋아요 누르기
            self.go_to_profile_page(userName)
            # TODO: 프로필에 '오픈톡','부업문의, 소액투자, 수익금, 재태크, 재택근무' 등의 단어를 포함한다면 제외하도록 추가.
            random_wait_time()

            profil_area = self.browser.find_element_by_class_name('-vDIg')

            try:
                if not has_caution_words(self, profil_area.text):
                    self.click_like_recent()

            except NoSuchElementException:
                print("End of feed.")
            pass

            random_wait_time()

            # 팔로잉 누르기
            # self.click_following_button()
            # 메시지 남기기 BASIC_MESSAGE ( baseUserName+"님 보고 왔어요. 먼저 선팔하고 갑니다 ^^ " + BASIC_MESSAGE)
            # self.click_message_button()

    def click_like_recent(self):
        # 최근 게시물 선택해서 '좋아요' 클릭
        time.sleep(3)
        selected_ele = self.browser.find_element_by_xpath('//article/div/div/div[1]/div[1]/a')
        click_element(selected_ele)
        # self.nextFeed()

        for a in range(5):
            # 좋아요 누르기
            time.sleep(3)
            like_list = self.browser.find_elements_by_xpath('//article//section/span/button')
            click_element(like_list[0])

            # 다음 피드로 이동하기
            next_feed_selector = 'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow'
            click_by_css_selector(self, next_feed_selector)
