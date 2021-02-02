import config
import telepot
from Insta.Like_recents import *


class Telegram():
    def __init__(self):
        print("텔레그램 구동합니다.")
        self.token = config.TELEGRAM_BOT_TOKKEN
        self.bot = telepot.Bot(self.token)
        self.bot.message_loop(self.start_telegram)
        while 1:
            pass

    def start_telegram(self, msg, info=None):
        tel_text = msg['text']
        chat_id = msg['chat']['id']

        if tel_text == "반사":
            self.bot.sendMessage(chat_id, "로그인... 잠시만 기다려주세요")
            LikeRecents()
            self.bot.sendMessage(chat_id, "좋아요 반사 완료")

        if tel_text == "시작":
            # TODO: 잠자는 맥을 깨워 봇을 활성화 하자 \n 맥의 활성화 시간 12시 ~ 1시 (점심시간)
            pass