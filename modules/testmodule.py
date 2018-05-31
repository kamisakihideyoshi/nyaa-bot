# coding=utf-8
# from linebot.models import (TextSendMessage, ImageSendMessage, StickerSendMessage, TemplateSendMessage)
import requests

from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ImagemapSendMessage
)

from linebot.models import (
    ButtonsTemplate,
    ConfirmTemplate,
    CarouselTemplate,
    ImageCarouselTemplate
)

from linebot.models import (
    PostbackTemplateAction,
    MessageTemplateAction,
    URITemplateAction,
    URIImagemapAction,
    MessageImagemapAction
)

from linebot.models import (
    CarouselColumn,
    ImageCarouselColumn
)

from linebot.models import (
    BaseSize,
    ImagemapArea
)

from .base import DataType, ModuleBase, ModuleData


class NotATestModule(ModuleBase):
    keywords = ['OωO', ' {1}NotTest']

    def text_message_user(self, reply_token, text_message, profile):
        if not 'NotTest' in text_message:
            message = TextSendMessage('(=OωO=)')
            self.reply(reply_token, message)
            return

        user_id = profile.user_id
        if user_id is None:
            user_id = self._get_provider_id()

        if user_id != self._get_provider_id():
            message = TextSendMessage('にゃー！\n(Permission denied)')
            self.reply(reply_token, message)
            return

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

        self.reply(reply_token, test_messages)
        return
