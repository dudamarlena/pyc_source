# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\RssReader\tests.py
# Compiled at: 2019-12-13 13:38:18
# Size of source mod 2**32: 2338 bytes
from unittest import TestCase
from rssaggregator import RssParser
from getting_news import get_cached_news
import json

class TestRssAggregator(TestCase):

    def test_parse_none_url_return_empty_dict(self):
        rss_object = RssParser('')
        self.assertEqual(rss_object.news, {})

    def test_parse_incorrect_url_return_empty_dict(self):
        rss_object = RssParser('123')
        self.assertEqual(rss_object.news, {})

    def test_parse_with_limit_none_url_return_empty_dict(self):
        rss_object = RssParser('', 3)
        self.assertEqual(rss_object.news, {})

    def test_parse_with_limit_incorrect_url_return_empty_dict(self):
        rss_object = RssParser('123', 5)
        self.assertEqual(rss_object.news, {})

    def test_convert_to_jason_none_url_return_empty_dict(self):
        rss_object = RssParser('')
        self.assertEqual(rss_object.convert_to_json(), '{}')

    def test_convert_to_jason_incorrect_url_return_empty_dict(self):
        rss_object = RssParser('123')
        self.assertEqual(rss_object.convert_to_json(), '{}')

    def test_convert_to_jason_with_limit_none_url_return_empty_dict(self):
        rss_object = RssParser('', 10)
        self.assertEqual(rss_object.convert_to_json(), '{}')

    def test_convert_to_jason_with_limit_incorrect_url_return_empty_dict(self):
        rss_object = RssParser('123', 20)
        self.assertEqual(rss_object.convert_to_json(), '{}')


class TestCachingModule(TestCase):

    def test_get_cached_news_no_file_exception(self):
        self.assertRaises(Exception, get_cached_news('20191010'))

    def test_get_cached_news_without_date(self):
        file_name = 'database.txt'
        json_data = {'20191010': [
                      'Title:Britains Political Map Changes Color in Ways Few Could Imagine',
                      'Title:Thunberg calls for `fight for tomorrow&#39; at Italy protest']}
        with open(file_name, 'w') as (file):
            json.dump(json_data, file)
        result = [
         'Title:Britains Political Map Changes Color in Ways Few Could Imagine',
         'Title:Thunberg calls for `fight for tomorrow&#39; at Italy protest']
        news = get_cached_news('20191010')
        self.assertEqual(news, result)