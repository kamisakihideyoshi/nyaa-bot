# coding=UTF-8
# from app import line_bot_api
from linebot.models import *

from linebot import (
    LineBotApi, WebhookHandler
)
import random

trigger_keywords = ['OwO', 'OωO']
user_action = {}


meal_list = ['50 元飯包', '咖食堂', '佐賀', '八方雲集', '大餛飩',
             '媽祖麵館', '嵐迪義大利麵', '70 元送飲料', '麥當勞', '肯德基', '漢堡王']

# Channel Access Token
line_bot_api = LineBotApi(
    'your token')
# Channel Secret
handler = WebhookHandler('7fd55205b15b651aa01ac0f2b8fb358f')


def nyaa(profile, event):
    reply = '@' + profile.display_name + ' ' + 'にゃー'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


def test(profile, event):
    test_messages = [
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        ),
        TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Are you sure?',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    )
                ]
            )
        ),
        TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item1.jpg',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title='this is menu2',
                        text='description2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]
                    )
                ]
            )
        ),
        TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://example.com/item1.jpg',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://example.com/item2.jpg',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        ),
        ImagemapSendMessage(
            base_url='https://example.com/base',
            alt_text='this is an imagemap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://example.com/',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='hello',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
    ]
    temp_list = meal_list
    reply_list = []
    for i in range(3):
        reply_list.append(temp_list.pop(random.randint(0, len(temp_list) - 1)))
    reply_message = TemplateSendMessage(
        alt_text='にゃー (' + '@' + profile.display_name + ', 何を食べる？)',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='にゃー',
            text='(何を食べる？)',
            actions=[
                MessageTemplateAction(
                    label=reply_list[0],
                    text=reply_list[0] + 'がいい'
                ),
                MessageTemplateAction(
                    label=reply_list[1],
                    text=reply_list[1] + 'がいい'
                ),
                MessageTemplateAction(
                    label=reply_list[2],
                    text=reply_list[2] + 'がいい'
                ),
                MessageTemplateAction(
                    label='チェンジで',
                    text='チェンジで'
                )
            ]
        )
    )

    line_bot_api.reply_message(event.reply_token, reply_message)


def meal(token):
    temp_list = meal_list
    reply_list = []
    for i in range(3):
        reply_list.append(temp_list.pop(random.randint(0, len(temp_list) - 1)))
    reply_message = TemplateSendMessage(
        alt_text='にゃー (何を食べる？)',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='にゃー',
            text='(何を食べる？)',
            actions=[
                MessageTemplateAction(
                    label=reply_list[0],
                    text=reply_list[0] + 'がいい'
                ),
                MessageTemplateAction(
                    label=reply_list[1],
                    text=reply_list[1] + 'がいい'
                ),
                MessageTemplateAction(
                    label=reply_list[2],
                    text=reply_list[2] + 'がいい'
                )
            ]
        )
    )

    line_bot_api.reply_message(token, reply_message)
