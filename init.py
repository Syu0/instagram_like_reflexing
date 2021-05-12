#!/usr/bin/python
# -*- coding: utf-8 -*-
from Insta.Like_recents import LikeRecents
from Insta.Like_reflexing import LikeReflexing
from Insta.Scraping_followers import ScrapingFollowers
from Insta.Tag_followering import TagFollowering
from Telegram.telegram import Telegram


class Main():
    def __init__(self):
        print("시작합니다 \n")
        LikeRecents() # 홈피드의 게시글에 '좋아요'를 누릅니다.
        TagFollowering() # 태그를 지정하고, 태그를 가진 최근 게시물에 '좋아요'를 누릅니다.
        LikeReflexing()  # 최근 활동 버튼을 누른 뒤, 최근에 내 계정에 '좋아요'를 누른 계정에 찾아가 '좋아요 반사'를 합니다.
        ScrapingFollowers() # 지정한 계정의 팔로잉/팔로워 계정을 순회하며 '좋아요'를 누릅니다.
        #FilterUnableUser() # 부업계정이 있는지 보여줍니다.
        Telegram() # 텔레그램 기능을 활성화 합니다.


if __name__ == "__main__":
    Main()  # Main() class를 실행합니다.
