# coding=UTF-8
# import pkgutil
# import re
# import datetime

import os

import sys
import inspect
import glob
import importlib

import threading
import time
import queue

from modules.base import DataCenter, DataPriority, ModuleData, DataType

from os import listdir
from os.path import dirname, basename

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
# from linebot.models import *  # noqa

from linebot.models import (
    MessageEvent,
    PostbackEvent
)

from linebot.models import (
    Message,
    TextMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    FileMessage
)

feedback_queue = queue.PriorityQueue()
user_id_default = 'your user id'
app = Flask(__name__)

# Channel Secret
nyaa_handler = WebhookHandler('your secret')

print('\nLine bot starting OωO')

start_time = time.time()
module_dir = 'modules'
modules_path = glob.glob('./' + module_dir + '/*.py')
modules = []
for path in modules_path:
    if path.endswith('__init__.py'):
        continue

    module = module_dir + '/' + basename(path).replace('.py', '')
    modules.append(module.replace('/', '.'))

thread_list = []
queue_list = []

module_number = 0
for module in modules:
    importlib.import_module(module)
    for name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj):
            if obj.__module__ == module:
                submodule = obj()
                if not submodule.__class__.__base__.__name__ == "ModuleBase":
                    continue
                '''
                All obj here should inherited from class ModuleBase
                init with arguments: main_queue, feedback_queue and tag.
                '''
                queue_list.append(queue.PriorityQueue())
                submodule.set_queue(queue_list[module_number], feedback_queue,
                                    module_number)
                thread_list.append(submodule)
                module_number += 1

thread_list.append(DataCenter(queue_list, feedback_queue))

for thread in thread_list:
    # print(thread)
    thread.daemon = True
    thread.start()

print('Finish time:', time.time() - start_time, 's.')


@app.route("/callback", methods=['POST'])
def nyaa_callback():
    """Method that monitor all POST requests to nyaa-bot"""
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    if signature == 'Wake-up-OwO':
        return 'OK'

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # print('New POST request to nyaa-bot, body:', body)
    # print('signature:', signature)

    # handle webhook body
    try:
        nyaa_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@nyaa_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Method that process text massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_TEXT)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    """Method that process image massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_IMAGE)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    """Method that process video massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_VIDEO)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    """Method that process audio massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_AUDIO)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    """Method that process location massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_LOCATION)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    """Method that process sticker massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_STICKER)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    """Method that process file massage"""
    data = ModuleData(event, data_type=DataType.MESSAGE_FILE)
    feedback_queue.put((DataPriority.MESSAGE, data))


@nyaa_handler.add(PostbackEvent)
def handle_postback(event):
    """Method that process postback data"""
    data = ModuleData(event, data_type=DataType.POSTBACK)
    feedback_queue.put((DataPriority.MESSAGE, data))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
