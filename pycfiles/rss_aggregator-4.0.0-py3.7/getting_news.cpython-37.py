# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\RssReader\getting_news.py
# Compiled at: 2019-12-12 11:42:56
# Size of source mod 2**32: 513 bytes
import json

def get_cached_news(date):
    """Function that return cached news from given date"""
    try:
        cached_news = []
        with open('database.txt', 'r') as (f):
            json_dict = json.loads(f.read())
            if date in json_dict:
                for news in json_dict[date]:
                    cached_news.append(news)

                return cached_news
    except (FileNotFoundError, Exception) as e:
        try:
            raise Exception('Error getting cached news: {}'.format(e))
        finally:
            e = None
            del e