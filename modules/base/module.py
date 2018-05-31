# coding=utf-8
import threading
import queue
import time

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import (TextSendMessage, ImageSendMessage)

from .data import DataType, DataPriority, ModuleData


class ModuleBase(threading.Thread):
    """The base class of all bot modules"""

    __line_bot_api = LineBotApi('your token')
    __provider_user_id = 'your user id'

    keywords = None  # type: list
    alias_list = {}  # type: dict

    def __init__(self):
        threading.Thread.__init__(self)

    def set_queue(self, main_queue: queue.PriorityQueue, feedback_queue: queue.PriorityQueue,
                  tag: int):

        self.name = self.__class__.__name__
        print('Initailizing... --', self.name)
        self.main_queue = main_queue
        self.feedback_queue = feedback_queue
        self.tag = tag

    def __str__(self):
        return self.name

    def _sync_alias(self, data: dict):
        self.alias_list.update(data)
        print('Alias list updated --', self.name)

    def clock(self, date_string: str):
        # print('Tick tock, tick tock... --', self.name)
        pass

    def text_message_user(self, reply_token, text_message, profile):
        pass

    def text_message_group(self, reply_token, text_message, profile):
        pass

    def text_message_room(self, reply_token, text_message, profile):
        pass

    def text_message_all(self, reply_token, text_message, profile):
        pass

    def redirect_data(self, data):
        pass

    def get_alias(self, alias):
        if not alias in self.alias_list:
            return None
        return self.alias_list[alias]

    def _get_provider_id(self):
        return self.__provider_user_id

    def _get_bot_api(self):
        return self.__line_bot_api

    def redirect(self, data, module_name):
        self.feedback_queue.put((DataPriority.MODULE, ModuleData(
            data, data_type=DataType.REDIRECT, redirect_module=module_name)))
        pass

    def reply(self, reply_token, messages):
        self.__line_bot_api.reply_message(reply_token, messages)

    def push(self, to, messages):
        self.__line_bot_api.push_message(to, messages)

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
                    user_id = self.__provider_user_id

                print('user id: ', user_id)

                if source_type == 'user':
                    profile = self.__line_bot_api.get_profile(user_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        reply_token = data.reply_token
                        threading._start_new_thread(
                            self.text_message_all, (reply_token, data.message.text, profile))
                        threading._start_new_thread(
                            self.text_message_user, (reply_token, data.message.text, profile))

                    continue

                if source_type == 'group':
                    group_id = data.source.group_id
                    if user_id == self.__provider_user_id:
                        profile = self.__line_bot_api.get_profile(user_id)
                    else:
                        profile = self.__line_bot_api.get_group_member_profile(
                            group_id, user_id)

                    print('group id: ', group_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        reply_token = data.reply_token
                        threading._start_new_thread(
                            self.text_message_all, (reply_token, data.message.text.replace('@ ', ''), profile))
                        threading._start_new_thread(
                            self.text_message_group, (reply_token, data.message.text.replace('@ ', ''), profile))

                    continue

                if source_type == 'room':
                    room_id = data.source.room_id
                    if user_id == self.__provider_user_id:
                        profile = self.__line_bot_api.get_profile(user_id)
                    else:
                        profile = self.__line_bot_api.get_room_member_profile(
                            room_id, user_id)
                    print('room id: ', room_id)

                    if data_type == DataType.MESSAGE_TEXT:
                        reply_token = data.reply_token
                        threading._start_new_thread(
                            self.text_message_all, (reply_token, data.message.text.replace('@ ', ''), profile))
                        threading._start_new_thread(
                            self.text_message_room, (reply_token, data.message.text.replace('@ ', ''), profile))

                    continue

            else:
                time.sleep(0.2)
