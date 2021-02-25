#!/usr/bin/python
# -*- coding: utf-8 -*-
from Insta.Like_recents import LikeRecents
from Insta.Like_reflexing import LikeReflexing
from Insta.Tag_followering import TagFollowering
from Telegram.telegram import Telegram


class Main():
    def __init__(self):
        print("시작합니다 \n")
        # LikeRecents()
        # LikeReflexing()
        # TagFollowering()
        Telegram()


if __name__ == "__main__":
    Main()  # Main() class를 실행합니다.
