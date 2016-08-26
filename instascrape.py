#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from nested_lookup import nested_lookup


class Oracle:
    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    def __init__(self):
        self.s = requests.Session()
        self.s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})
        self.s.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self.accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/explore/tags/lifeatshopify/',
                               'User-Agent': self.user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        self.csrftoken = r.cookies['csrftoken']

    def get_images(self):
        r = self.s.get(self.url_tag + "lifeatshopify/")
        text = r.text

        finder_text_start = ('<script type="text/javascript">'
                             'window._sharedData = ')
        finder_text_start_len = len(finder_text_start)-1
        finder_text_end = ';</script>'

        all_data_start = text.find(finder_text_start)
        all_data_end = text.find(finder_text_end, all_data_start + 1)
        json_str = text[(all_data_start + finder_text_start_len + 1):all_data_end]
        all_data = json.loads(json_str)
        img_sources = nested_lookup('display_src', all_data)
        end_cursor = nested_lookup('end_cursor', all_data)[0]
        print("(initial) total pictures scraped: " + str(len(img_sources)))
        print(img_sources)
        return img_sources, end_cursor

    def get_more(self, last_end_cursor):
        more_url = r"https://www.instagram.com/query/?q=ig_hashtag(lifeatshopify)+%7B+media.after(" + last_end_cursor + r"%2C+11)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++comments_disabled%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=tags%3A%3Ashow"
        r = self.s.get(more_url)
        res = json.loads(r.text)
        img_sources = nested_lookup('display_src', res)
        end_cursor = nested_lookup('end_cursor', res)[0]
        print("(more) total pictures scraped: " + str(len(img_sources)))
        print(img_sources)
        return img_sources, end_cursor

if __name__ == '__main__':
    bot = Oracle()
    images, end_cursor = bot.get_images()
    while len(images):
        images, end_cursor = bot.get_more(end_cursor)
