# coding=UTF-8
import re
import random
import logging
import urllib.parse
import urllib.request
import urllib.error

from linebot.models import (TextSendMessage, ImageSendMessage)
from .base import DataType, ModuleBase, ModuleData

trigger_keywords = ['cat', '貓', 'ねこ', 'ぬこ', '猫']

main_keywords = ['ねこ', 'ぬこ']
supplemented_keywords = ['かわいい', 'おもしろ', '和む']


def download_page(url):
    """download raw content of the page

    Args:
        url (str): url of the page

    Returns:
        raw content of the page
    """
    try:
        headers = {}
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        headers['Referer'] = 'https://www.google.com'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return str(resp.read())
    except Exception as e:
        print('error while downloading page {0}'.format(url))
        print('error:', e)
        logging.error('error while downloading page {0}'.format(url))
        return None


def parse_page(url):
    """parge the page and get all the links of images, max number is 100 due to limit by google

    Args:
        url (str): url of the page

    Returns:
        A set containing the urls of images
    """
    page_content = download_page(url)
    if page_content:
        link_list = re.findall('"ou":"(.*?)"', page_content)
        if len(link_list) == 0:
            print('get 0 links from page {0}'.format(url))
            logging.info('get 0 links from page {0}'.format(url))
            return set()
        else:
            return set(link_list)
    else:
        return set()


def get_image_link():
    """get image link with one main keyword and multiple supplemented keywords

    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords

    Returns:
        A image link
    """
    image_links = set()
    supplemented_keyword = urllib.parse.quote(
        supplemented_keywords[random.randint(0,
                                             len(supplemented_keywords) - 1)],
        safe='')
    main_keyword = urllib.parse.quote(
        main_keywords[random.randint(0,
                                     len(main_keywords) - 1)], safe='')

    # print('the theme of cats: ' + supplemented_keyword)

    search_query = (main_keyword + ' ' + supplemented_keyword).replace(
        ' ', '%20')
    url = 'https://www.google.com/search?q=' + \
        search_query + '&source=lnms&tbm=isch'
    image_links = image_links.union(parse_page(url))

    image_link = list(image_links)[random.randint(0, len(image_links) - 1)]
    # print('link:' + image_link)

    while 'https://' not in image_link or r'\\u' in image_link or '.jpg' not in image_link:
        image_link = list(image_links)[random.randint(0, len(image_links) - 1)]
        # print('link:' + image_link)

    return image_link


class CatImage(ModuleBase):
    keywords = ['Cat', 'cat', '貓', '猫', 'ねこ', 'ぬこ']

    def text_message_user(self, reply_token, text_message, profile):
        pass

    def text_message_group(self, reply_token, text_message, profile):
        pass

    def text_message_room(self, reply_token, text_message, profile):
        pass

    def text_message_all(self, reply_token, text_message, profile):
        image_link = get_image_link()
        message = ImageSendMessage(
            original_content_url=image_link, preview_image_url=image_link)
        self.reply(reply_token, message)

    def run(self):
        ModuleBase.run(self)
