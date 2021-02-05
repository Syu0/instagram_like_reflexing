#!/usr/bin/python
# -*- coding: utf-8 -*-
from Insta.Like_recents import LikeRecents
from Insta.Like_reflexing import LikeReflexing
from Like_recents.telegram import Telegram


class Main():
    def __init__(self):
        print("시작합니다 \n")
        Telegram()
        # LikeRecents()
        # LikeReflexing()


if __name__ == "__main__":
    Main()  # Main() class를 실행합니다.
