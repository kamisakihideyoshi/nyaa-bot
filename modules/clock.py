# coding=utf-8
# from linebot.models import (TextSendMessage, ImageSendMessage, StickerSendMessage, TemplateSendMessage)
import time
import datetime
import requests

# from linebot.models import *  # noqa

from .base import DataType, DataPriority, ModuleBase, ModuleData


class Clock(ModuleBase):
    def _wake_up(self):
        headers = {'X-Line-Signature': 'Wake-up-OwO'}
        requests.post(
            'your callback url', headers=headers)

        # print('Self wake-up signal sent --', self.name)

    def run(self):
        # Send init data to data center for identification:
        init_data = ModuleData(
            data=self.keywords,
            data_type=DataType.INIT,
            module_tag=self.tag,
            module_name=self.name)
        self.feedback_queue.put((DataPriority.SYSTEM, init_data))
        # print('Module', self.name, 'sent init data')

        self.count = 0
        while True:
            time.sleep(60)
            if self.count > 20:
                self._wake_up()
                self.count = 0

            current_date = datetime.datetime.now()
            current_date_string = current_date.strftime(r'%m%d%H%M%S')
            self.feedback_queue.put(
                (DataPriority.MODULE, ModuleData(data=current_date_string, data_type=DataType.CLOCK)))
            self.count += 1
