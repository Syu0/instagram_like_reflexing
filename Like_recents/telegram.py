import textwrap

import telepot
from Insta.Like_recents import *


class Telegram():
    def __init__(self):
        print("텔레그램 구동합니다.")
        self.token = config.TELEGRAM_BOT_TOKKEN
        self.bot = telepot.Bot(self.token)
        self.bot.message_loop(self.message_agent)
        while 1:
            pass

    def message_agent(self, msg, info=None):
        tel_text = msg['text']
        chat_id = msg['chat']['id']

        if tel_text == "노크":
            self.bot.sendMessage(chat_id, "최근 피드들의 하트를 누릅니다. 약 20분 정도 소요되요.")
            LikeRecents()
            self.bot.sendMessage(chat_id, "하트 누르기 완료")

        if tel_text == "뭐하지":
            manual = textwrap.dedent("""
                    노크 : 최근 피드들의 하트를 누릅니다.(약 20분 소요).
                    뭐하지 : 사용할 수 있는 단어들을 알려줍니다.
                    """)
            self.bot.sendMessage(chat_id, manual)

        else:
            self.bot.sendMessage(chat_id, "노크줘 / 뭐하지 라고 해주세요. 최근 피드들의 하트를 누릅니다.(약 20분 소요)")
