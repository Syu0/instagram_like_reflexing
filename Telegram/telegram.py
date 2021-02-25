import re
import textwrap

import telepot

import config
from Insta.Like_recents import LikeRecents
from Insta.Like_reflexing import LikeReflexing
from Insta.Tag_followering import TagFollowering


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
        input_tag_text = re.compile('.* 탐색')  # 태그탐색

        if tel_text == "노크":
            self.bot.sendMessage(chat_id, "최근 피드들의 하트를 누릅니다. 약 20분 정도 소요되요.")
            LikeRecents()
            self.bot.sendMessage(chat_id, "하트 누르기 완료")

        if tel_text == "반사":
            self.bot.sendMessage(chat_id, "좋아요 눌러준 계정에 하트를 눌러줍니다. 완료되면 알려줄게요")
            result = LikeReflexing()

            self.bot.sendMessage(chat_id, str(result.newFollower))
            self.bot.sendMessage(chat_id, str(result.newComments))
            self.bot.sendMessage(chat_id, "하트 누르기 완료")

        # 태그탐색 ' ㅌㅌㅌ 탐색 '
        if input_tag_text.match(tel_text):
            custom_text = tel_text[0:-3]
            custom_text = ''.join(custom_text)
            self.bot.sendMessage(chat_id, '{' + custom_text + "} 태그를 검색하고, 최근 게시물 10개에 좋아요를 누릅니다. 완료되면 알려줄게요")
            TagFollowering(custom_text)
            self.bot.sendMessage(chat_id, '{' + custom_text + '} 태그를 검색 완료')

        if tel_text == "추천탐색":
            self.bot.sendMessage(chat_id, "추천 태그를 이용해 최근 게시물 10개에 좋아요를 누릅니다.")
            TagFollowering()
            # TODO 총 몇명의 방문을 했는지 알려주면 좋겠다.

            self.bot.sendMessage(chat_id, "추천탐색 완료")

        # TODO : 태그검색 + 프로필 방문 + 팔로잉 + 좋아요 3개 기능 추가

        if tel_text == "추천태그":
            self.bot.sendMessage(chat_id, "추천태그를 알려줄게요. 마음에 들면 '추천탐색'을 실행하세요.")
            # TODO: 계정별로 태그를 다르게 추천한다.
            self.bot.sendMessage(chat_id, "인업같이|씨클맞팔|책육아|파이썬|")

        if tel_text == "뭐하지":
            manual = textwrap.dedent("""
                    노크 : 최근 피드들의 하트를 누릅니다.(약 20분 소요).
                    
                    반사 : 좋아요 눌러준 계정에 받은만큼 하트를 눌러줍니다. 
                    
                    뭐하지 : 사용할 수 있는 단어들을 알려줍니다.
                    
                    {검색할태그} 탐색 : 예) '블럭놀이 탐색' 이라고 입력하면 '블럭놀이'를 검색합니다. 결과화면의 최근 게시물 10개에 좋아요를 누릅니다.
                    
                    추천탐색 : 미리 지정된 추천태그를 검색하고, 최근 게시물을 남긴 사용자의 프로필을 방문합니다.
                    
                    추천태그 : 추천태그가 어떤건지 보여줍니다. 왼쪽 첫번째 태그가 사용됩니다.
                    """)
            self.bot.sendMessage(chat_id, manual)
        else:
            self.bot.sendMessage(chat_id, "노크 | 반사 | {검색할태그} 탐색 | 추천탐색 | 추천태그 | 뭐하지(도움말) 라고 해보세요.")
