# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/tests/search/test_search_appledaily.py
# Compiled at: 2019-08-13 05:11:25
# Size of source mod 2**32: 1161 bytes
"""
蘋果日報搜尋測試
"""
import unittest
from twnews.search import NewsSearch

class TestAppleDaily(unittest.TestCase):
    __doc__ = '\n    蘋果日報搜尋測試\n    '

    def setUp(self):
        self.keyword = '上吊'
        self.nsearch = NewsSearch('appledaily', limit=10)

    def test_01_filter_title(self):
        """
        測試蘋果日報搜尋
        """
        results = self.nsearch.by_keyword((self.keyword), title_only=True).to_dict_list()
        for topic in results:
            if '上吊' not in topic['title']:
                self.fail('標題必須含有 "上吊"')

    def test_02_search_and_soup(self):
        """
        測試蘋果日報搜尋+分解
        """
        nsoups = self.nsearch.by_keyword(self.keyword).to_soup_list()
        for nsoup in nsoups:
            if nsoup.contents() is None:
                msg = nsoup.path.startswith('https://home.appledaily.com.tw') or '內文不可為 None, URL={}'.format(nsoup.path)
                self.fail(msg)