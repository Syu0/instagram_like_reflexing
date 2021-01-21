import config
import telepot
from Insta.Instagram import *


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

        if tel_text == "로그인":
            self.bot.sendMessage(chat_id, "로그인... 잠시만 기다려주세요")
            self.Instagram.login()
            self.bot.sendMessage(chat_id, "로그인 완료")
