# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/tests/search/test_search_cna.py
# Compiled at: 2019-08-13 05:10:12
# Size of source mod 2**32: 886 bytes
"""
中央社搜尋測試
"""
import unittest
from twnews.search import NewsSearch

class TestCna(unittest.TestCase):
    __doc__ = '\n    中央社搜尋測試\n    '

    def setUp(self):
        self.keyword = '上吊'
        self.nsearch = NewsSearch('cna', limit=10)

    def test_01_filter_title(self):
        """
        測試中央社搜尋
        """
        results = self.nsearch.by_keyword((self.keyword), title_only=True).to_dict_list()
        for topic in results:
            if '上吊' not in topic['title']:
                self.fail('標題必須含有 "上吊"')

    def test_02_search_and_soup(self):
        """
        測試中央社搜尋+分解
        """
        nsoups = self.nsearch.by_keyword(self.keyword).to_soup_list()
        for nsoup in nsoups:
            if nsoup.contents() is None:
                self.fail('內文不可為 None')