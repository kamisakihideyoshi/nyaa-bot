# coding=utf-8
import re

from linebot.models import TextSendMessage

from .base import DataType, DataPriority, ModuleBase, ModuleData


class Alias(ModuleBase):
    keywords = ['--alias']
    alias_list = {}

    def run(self):
        ModuleBase.run(self)

    def text_message_user(self, reply_token, text_message, profile):
        if not re.match(r'--alias {1}\w+ {1}\w+', text_message):
            reply = 'にゃ？ \n(Usage: --alias <user id | group id> <alias you want to set>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

        alias_info = text_message.split(' ')  # type: list
        self.alias_list[alias_info[1]] = alias_info[2]

        # Sync alias list to all modules:
        self.feedback_queue.put((DataPriority.MODULE, ModuleData(
            self.alias_list, data_type=DataType.ALIAS)))

        reply = 'にゃー \n(Set alias ' + \
            alias_info[2] + ' to ' + alias_info[1] + ')'
        self.reply(reply_token, TextSendMessage(text=reply))

    def text_message_group(self, reply_token, text_message, profile):
        user_name = profile.display_name

        if not re.match(r'--alias {1}\w+ {1}\w+', text_message):
            reply = '@ ' + user_name + ' にゃ？ \n(Usage: --alias' \
                    ' <user id | group id> <alias you want to set>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

        alias_info = text_message.split(' ')  # type: list
        self.alias_list[alias_info[1]] = alias_info[2]

        # Sync alias list to all modules:
        self.feedback_queue.put((DataPriority.MODULE, ModuleData(
            self.alias_list, data_type=DataType.ALIAS)))

        reply = '@ ' + user_name + \
            ' にゃー \n(Set alias ' + alias_info[2] + ' to ' + alias_info[1] + ')'
        self.reply(reply_token, TextSendMessage(text=reply))

    def text_message_room(self, reply_token, text_message, profile):
        user_name = profile.display_name

        if not re.match(r'--alias {1}\w+ {1}\w+', text_message):
            reply = '@ ' + user_name + ' にゃ？ \n(Usage: --alias' \
                    ' <user id | group id> <alias you want to set>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

        alias_info = text_message.split(' ')  # type: list
        self.alias_list[alias_info[1]] = alias_info[2]

        # Sync alias list to all modules:
        self.feedback_queue.put((DataPriority.MODULE, ModuleData(
            self.alias_list, data_type=DataType.ALIAS)))

        reply = '@ ' + user_name + \
            ' にゃー \n(Set alias ' + alias_info[2] + ' to ' + alias_info[1] + ')'
        self.reply(reply_token, TextSendMessage(text=reply))
