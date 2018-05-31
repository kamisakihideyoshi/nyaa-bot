# coding=utf-8
import threading
import queue
import time

import re

from .data import DataType, DataPriority, ModuleData

from linebot import LineBotApi
from linebot.models import TextSendMessage


class DataCenter(threading.Thread):
    __line_bot_api = LineBotApi('your token')
    __user_id_default = 'your user id'

    def __init__(self, main_queues, feedback_queue: queue.Queue):
        threading.Thread.__init__(self)
        self.name = self.__class__.__name__
        self.feedback_queue = feedback_queue
        self.main_queue_list = []
        self.module_list = {}
        self.keyword_list = {}

        for main_queue in main_queues:
            self.main_queue_list.append(main_queue)

    def _init_module(self, received_data):
        # self.module_list[received_data.name] = received_data.tag
        self.module_list[received_data.name] = self.main_queue_list[received_data.tag]
        print('Received init data from:', received_data.name)

        if received_data.data:
            # print(received_data.data)
            # for keyword in received_data.data:
            #     self.keyword_list[keyword] = received_data.name
            self.keyword_list[received_data.name] = received_data.data

        # self.main_queue_list[self.module_list[received_data.name]].put(
        #     (DataPriority.SYSTEM, ModuleData()))
        self.module_list[received_data.name].put(
            (DataPriority.SYSTEM, ModuleData()))

    def _process_text_message(self, received_data):
        try:
            event = received_data.data  # type: Event
            message = event.message.text  # type: str
            print('\nMessage receive:', message)
        except AttributeError:
            print('WTF OωO!? --', self.name)

        source_type = event.source.type
        if source_type != 'user':
            if not re.match(r'@ .+', message):
                print('Calling pattern not match')
                # self.main_queue_list[self.module_list['General']].put(
                #     (DataPriority.MESSAGE, received_data))
                self.module_list['General'].put(
                    (DataPriority.MESSAGE, received_data))
                print('Send data to module: General --', self.name)
                return

            message.replace('@ ', '')

        keyword_matched = False
        for module_name, keywords in self.keyword_list.items():
            for keyword in keywords:
                # if keyword in message:
                if re.findall(keyword, message):
                    keyword_matched = True
                    # self.main_queue_list[self.module_list[module_name]].put(
                    #     (DataPriority.MESSAGE, received_data))
                    self.module_list[module_name].put(
                        (DataPriority.MESSAGE, received_data))
                    print('Send data to module:', module_name, '--', self.name)
                    return

        if not keyword_matched:
            # self.main_queue_list[self.module_list['General']].put(
            #     (DataPriority.MESSAGE, received_data))
            self.module_list['General'].put(
                (DataPriority.MESSAGE, received_data))
            print('Send data to module: General --', self.name)
            return

    def _redirect_data(self, received_data):
        redirect_module = received_data.redirect
        if redirect_module is None:
            print('Redirection error: No redirect module name --', self.name)
            return

        if redirect_module not in self.module_list:
            print('Redirection error: No module', redirect_module, '--',
                  self.name)
            return

        self.module_list[redirect_module].put(
            (DataPriority.MODULE, received_data))
        print('Redirect data to module:', redirect_module, '--', self.name)

    def _sync_alias(self, received_data):
        print('Updating alias... --', self.name)
        for main_queue in self.main_queue_list:
            main_queue.put((DataPriority.MODULE, received_data))

    def _clock(self, received_data):
        # print('Send clock signal... --', self.name)
        for main_queue in self.main_queue_list:
            main_queue.put((DataPriority.MODULE, received_data))

    def run(self):
        while True:
            if self.feedback_queue.qsize() > 0:
                raw_data = self.feedback_queue.get()
                received_data = raw_data[1]  # type: ModuleData

                # print('Data type:', received_data.data_type)
                if received_data.data_type == DataType.INIT:
                    self._init_module(received_data)
                    continue

                if received_data.data_type == DataType.ALIAS:
                    self._sync_alias(received_data)
                    continue

                if received_data.data_type == DataType.CLOCK:
                    self._clock(received_data)
                    continue

                if received_data.data_type == DataType.HELP:
                    if received_data.redirect:
                        self._redirect_data(received_data)
                        continue

                    usage_text = 'にゃー\n(\nkeywords:\n'
                    for module_name in self.module_list.keys():
                        if module_name in self.keyword_list:
                            usage_text += module_name + ' -- '
                            keywords = self.keyword_list[module_name]
                            for keyword in keywords:
                                matches = re.findall('{.+}', keyword)
                                for match in matches:
                                    keyword = keyword.replace(match, '')
                                usage_text += keyword + ' | '
                            usage_text += '\n'
                    usage_text += ')'
                    reply_token = received_data.data
                    help_message = TextSendMessage(usage_text)
                    self.__line_bot_api.reply_message(reply_token,
                                                      help_message)
                    continue

                if received_data.data_type == DataType.MESSAGE_TEXT:
                    self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_IMAGE:
                    print('Image message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_VIDEO:
                    print('Video message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_AUDIO:
                    print('Audio message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_LOCATION:
                    print('Location message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_STICKER:
                    print('Sticker message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.MESSAGE_FILE:
                    print('File message received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                if received_data.data_type == DataType.POSTBACK:
                    print('Postback data received --', self.name)
                    # self._process_text_message(received_data)
                    continue

                # if received_data.data_type == DataType.REPLY:
                #     print('Reply function is not implemented yet OωO --',
                #           self.name)
                #     continue

                # if received_data.data_type == DataType.PUSH_USER:
                #     print(
                #         'Push to user function is not implemented yet OωO --',
                #         self.name)
                #     continue

                # if received_data.data_type == DataType.PUSH_GROUP:
                #     print(
                #         'Push to group function is not implemented yet OωO --',
                #         self.name)
                #     continue
                # if received_data.data_type == DataType.PUSH_ROOM:
                #     print(
                #         'Push to room function is not implemented yet OωO --',
                #         self.name)
                #     continue

                if received_data.data_type == DataType.REDIRECT:
                    self._redirect_data(received_data)
                    continue
            else:
                time.sleep(0.2)
