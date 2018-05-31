# coding=utf-8
import threading
# import queue
import time
import re

from linebot import LineBotApi
from linebot.models import TextSendMessage

from .base import DataType, DataPriority, ModuleData, ModuleBase


class General(ModuleBase):
    def text_message_unmatched_all(self, reply_token, text_message, profile):
        pass

    def text_message_unmatched_user(self, reply_token, text_message, profile):
        if text_message == '抽':
            message = TextSendMessage('にゃー！\n(不讓你抽！)')
            self.reply(reply_token, message)

        print('Message ignored')

    def text_message_unmatched_group(self, reply_token, text_message, profile):
        if text_message == '抽':
            user_name = profile.display_name
            message = TextSendMessage('@' + user_name + ' にゃー！\n(不讓你抽！)')
            self.reply(reply_token, message)

        print('Message ignored')

    def text_message_unmatched_room(self, reply_token, text_message, profile):
        if text_message == '抽':
            user_name = profile.display_name
            message = TextSendMessage('@' + user_name + ' にゃー！\n(不讓你抽！)')
            self.reply(reply_token, message)

        print('Message ignored')

    def text_message_all(self, reply_token, text_message, profile):
        if text_message == '--help':
            print('This is a help message , return data to DataCenter --',
                  self.name)
            self.feedback_queue.put(
                (DataPriority.MODULE, ModuleData(reply_token, data_type=DataType.HELP)))
            return

        message = TextSendMessage('にゃー？')
        self.reply(reply_token, message)

    def run(self):
        # Send init data to data center for identification:
        init_data = ModuleData(
            data=self.keywords,
            data_type=DataType.INIT,
            module_tag=self.tag,
            module_name=self.name)
        self.feedback_queue.put((DataPriority.SYSTEM, init_data))

        # Start receiving data:
        while True:
            if self.main_queue.qsize() > 0:
                raw_data = self.main_queue.get()
                module_data = raw_data[1]  # type: ModuleData

                data = module_data.data
                data_type = module_data.data_type

                if data is None:
                    print('WTF OωO!? --', self.name)
                    continue

                if data_type == DataType.REDIRECT:
                    threading._start_new_thread(
                        self.redirect_data, (module_data,))
                    continue

                if data_type == DataType.ALIAS:
                    threading._start_new_thread(self._sync_alias, (data,))
                    continue

                if data_type == DataType.CLOCK:
                    threading._start_new_thread(self.clock, (data,))
                    continue

                print('This data have something inside OωO --', self.name)
                print('Type:', data_type)

                source_type = data.source.type
                user_id = data.source.user_id
                if user_id is None:
                    user_id = self._get_provider_id()

                print('user id: ', user_id)

                if source_type == 'user':
                    profile = self._get_bot_api().get_profile(
                        user_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        reply_token = data.reply_token
                        threading._start_new_thread(
                            self.text_message_unmatched_user, (reply_token, data.message.text, profile))
                        threading._start_new_thread(
                            self.text_message_all, (reply_token, data.message.text, profile))
                        threading._start_new_thread(
                            self.text_message_user, (reply_token, data.message.text, profile))

                    continue

                if source_type == 'group':
                    group_id = data.source.group_id
                    if user_id == self._get_provider_id():
                        profile = self._get_bot_api().get_profile(
                            user_id)
                    else:
                        profile = self._get_bot_api().get_group_member_profile(
                            group_id, user_id)
                    print('group id: ', group_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        text_message = data.message.text
                        reply_token = data.reply_token
                        if not re.match(r'@ \S+', text_message):

                            threading._start_new_thread(
                                self.text_message_unmatched_group, (reply_token, text_message.replace('@ ', ''), profile))
                            continue

                        threading._start_new_thread(
                            self.text_message_all, (reply_token, text_message.replace('@ ', ''), profile))
                        threading._start_new_thread(
                            self.text_message_group, (reply_token, text_message.replace('@ ', ''), profile))

                    continue

                if source_type == 'room':
                    room_id = data.source.room_id
                    if user_id == self._get_provider_id():
                        profile = self._get_bot_api().get_profile(
                            user_id)
                    else:
                        profile = self._get_bot_api().get_room_member_profile(
                            room_id, user_id)
                    print('room id: ', room_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        text_message = data.message.text
                        reply_token = data.reply_token
                        if not re.match(r'@ \S+', text_message):
                            threading._start_new_thread(
                                self.text_message_unmatched_user, (reply_token, text_message.replace('@ ', ''), profile))
                            continue

                        threading._start_new_thread(
                            self.text_message_all, (reply_token, text_message.replace('@ ', ''), profile))
                        threading._start_new_thread(
                            self.text_message_room, (reply_token, text_message.replace('@ ', ''), profile))

                    continue

            else:
                time.sleep(0.2)
