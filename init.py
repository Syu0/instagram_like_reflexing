# This is a sample Python script.
import config
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from msg.telegram import *  # tele 폴더의 telegram.py안의 모든 내용을 불러옵니다.


class Main():
    def __init__(self):
        print("시작합니다 \n")
        Instagram() #Insta() class
        #Telegram()  # Telegram() class를 실행합니다.


if __name__ == "__main__":
    Main()  # Main() class를 실행합니다.
