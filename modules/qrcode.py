import qrcode
import tempfile
import os
import re

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from linebot.models import (TextSendMessage, ImageSendMessage)
from .base import DataType, ModuleBase, ModuleData

client_id = 'your imgur client id'
client_secret = 'your imgur secret'

client = ImgurClient(client_id, client_secret)


def get_link(data):
    '''
    Generate a QR code from data string and return a Imgur link

    Arguments:
    data -- Data you want to save into QR code
    '''
    image = qrcode.make(data=data)

    temp = tempfile.NamedTemporaryFile()
    image.save(temp)

    config = {
        'name': 'Useless QR Code',
        'title': 'Useless QR Code',
        'description': 'Just an useless QR Code OωO'
    }

    try:
        print('The image should start upload if everything good...')
        upload_result = client.upload_from_path(
            temp.name, config=config, anon=True)
        print('Upload success OωO\nlink:', upload_result['link'])

        temp.close()
        return upload_result['link']

    except ImgurClientError as e:
        print('Oops, the process is going wrong (´･ω･`)')
        print('Error code ', e.status_code, ':', e.error_message)

        temp.close()
        return None


class QRCode(ModuleBase):
    keywords = ['--qrcode']

    def text_message_user(self, reply_token, text_message, profile):
        qrcode_pattern = '--qrcode .+'
        if re.match(qrcode_pattern, text_message):
            qrcode_arguments = re.split(' ', text_message, maxsplit=1)
            qrcode_data = qrcode_arguments[1]
            qrcode_link = get_link(qrcode_data)

            if qrcode_link:
                reply = 'にゃー'
                qrcode_reply = [
                    TextSendMessage(text=reply),
                    ImageSendMessage(
                        original_content_url=qrcode_link,
                        preview_image_url=qrcode_link)
                ]
                self.reply(reply_token, qrcode_reply)

                print('Reply with QR code')
                return
            else:
                reply = 'ニャー！ (Error occurred)'
                self.reply(reply_token, TextSendMessage(text=reply))

                print('qr_gen error: No QR code link generated,'
                      ' might be something went wrong.')
                return
        else:
            reply = 'にゃ？ \n(Usage: --qrcode <something you want to save into>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

    def text_message_group(self, reply_token, text_message, profile):
        user_name = profile.display_name
        qrcode_pattern = '--qrcode .+'
        if re.match(qrcode_pattern, text_message):
            qrcode_arguments = re.split(' ', text_message, maxsplit=1)
            qrcode_data = qrcode_arguments[1]
            qrcode_link = get_link(qrcode_data)

            if qrcode_link:
                reply = '@ ' + user_name + ' にゃー'
                qrcode_reply = [
                    TextSendMessage(text=reply),
                    ImageSendMessage(
                        original_content_url=qrcode_link,
                        preview_image_url=qrcode_link)
                ]
                self.reply(reply_token, qrcode_reply)

                print('Reply with QR code')
                return
            else:
                reply = '@ ' + user_name + ' ニャー！ (Error occurred)'
                self.reply(reply_token, TextSendMessage(text=reply))

                print('qr_gen error: No QR code link generated,'
                      ' might be something went wrong.')
                return
        else:
            reply = '@ ' + user_name + ' にゃ？ \n(Usage: --qrcode' \
                ' <something you want to save into>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

    def text_message_room(self, reply_token, text_message, profile):
        user_name = profile.display_name
        qrcode_pattern = '--qrcode .+'
        if re.match(qrcode_pattern, text_message):
            qrcode_arguments = re.split(' ', text_message, maxsplit=1)
            qrcode_data = qrcode_arguments[1]
            qrcode_link = get_link(qrcode_data)

            if qrcode_link:
                reply = '@ ' + user_name + ' にゃー'
                qrcode_reply = [
                    TextSendMessage(text=reply),
                    ImageSendMessage(
                        original_content_url=qrcode_link,
                        preview_image_url=qrcode_link)
                ]
                self.reply(reply_token, qrcode_reply)

                print('Reply with QR code')
                return
            else:
                reply = '@ ' + user_name + ' ニャー！ (Error occurred)'
                self.reply(reply_token, TextSendMessage(text=reply))

                print('qr_gen error: No QR code link generated,'
                      ' might be something went wrong.')
                return
        else:
            reply = '@ ' + user_name + ' にゃ？ \n(Usage: --qrcode' \
                ' <something you want to save into>)'
            self.reply(reply_token, TextSendMessage(text=reply))
            return

    def text_message_all(self, reply_token, text_message, profile):
        pass

    def run(self):
        ModuleBase.run(self)
