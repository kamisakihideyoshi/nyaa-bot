# coding=utf-8
import datetime
import re

from.base import DataType, ModuleBase, ModuleData
from.firebase import FirebaseApp, FirebaseAuth

from linebot.models import (
    TextSendMessage
)


class Calendar(ModuleBase):
    keywords = ['^calendar']

    def __init__(self):
        ModuleBase.__init__(self)
        self.auth = FirebaseAuth('your token',
                                 'your account', 'your password')
        self.firebase = FirebaseApp('nyaa-bot-501a2', auth=self.auth)

    def firebase_test(self):
        # year = date_string[0:3]
        # month = date_string[4:7]
        # hour = date_string[8:9]
        # minute = date_string[10:11]
        # second = date_string[12:13]

        # if hour == '08' and minute == '00' and second == '00':
        print(self.firebase.get(child='schedule'))

    def clock(self, date_string: str):
        # year = date_string[0:3]
        # month = date_string[4:7]
        # hour = date_string[8:9]
        # minute = date_string[10:11]
        # second = date_string[12:13]
        pass

    def text_message_user(self, reply_token, text_message, profile):
        user_id = profile.user_id

        if user_id != self._get_provider_id():
            message = TextSendMessage('にゃー！\n(Permission denied)')
            self.reply(reply_token, message)
            return

        if re.match('^calendar --test', text_message):
            self.firebase_test()

        if re.match('^calendar --show', text_message):
            pass

        if re.match('^calendar .+ /d{6}', text_message):
            pass

        message = TextSendMessage('(=OωO=)')
        self.reply(reply_token, message)
        return
