# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/tests/soup/test_soup_setn.py
# Compiled at: 2019-08-13 05:11:53
# Size of source mod 2**32: 2415 bytes
"""
三立新聞網分解測試
"""
import unittest, twnews.common
from twnews.soup import NewsSoup

class TestSetn(unittest.TestCase):
    __doc__ = '\n    三立新聞網分解測試\n    '

    def setUp(self):
        self.url = 'http://www.setn.com/News.aspx?NewsID=350370'
        self.dtf = '%Y-%m-%d %H:%M:%S'

    def test_01_sample(self):
        """
        測試三立新聞網樣本
        """
        pkgdir = twnews.common.get_package_dir()
        nsoup = NewsSoup(pkgdir + '/samples/setn.html.gz')
        self.assertEqual('setn', nsoup.channel)
        self.assertIn('與母爭吵疑失足墜樓\u3000男子送醫搶救不治', nsoup.title())
        self.assertEqual('2018-02-21 18:03:00', nsoup.date().strftime(self.dtf))
        self.assertEqual(None, nsoup.author())
        self.assertIn('新北市新店區中正路今（21）日下午3時許發生墜樓案件', nsoup.contents())

    def test_02_mobile(self):
        """
        測試三立新聞網行動版
        """
        nsoup = NewsSoup((self.url), refresh=True)
        self.assertEqual('setn', nsoup.channel)
        self.assertIn('與母爭吵疑失足墜樓\u3000男子送醫搶救不治', nsoup.title())
        self.assertEqual('2018-02-21 18:03:00', nsoup.date().strftime(self.dtf))
        self.assertEqual(None, nsoup.author())
        self.assertIn('新北市新店區中正路今（21）日下午3時許發生墜樓案件', nsoup.contents())

    def test_03_layouts(self):
        """
        測試三立新聞網的其他排版
        """
        layouts = [
         {'url':'https://www.setn.com/e/News.aspx?NewsID=460349', 
          'title':'不只想贏韓國！徐展元「分手女友」紅到美國…竟是切身之痛', 
          'date':'2018-11-22 17:29:00', 
          'author':'王奕棋', 
          'contents':'這個球就像變了心的女朋友，回不來了'}]
        for layout in layouts:
            nsoup = NewsSoup((layout['url']), refresh=True, proxy_first=True)
            self.assertEqual('setn', nsoup.channel)
            self.assertIn(layout['title'], nsoup.title())
            self.assertEqual(layout['date'], nsoup.date().strftime(self.dtf))
            self.assertEqual(layout['author'], nsoup.author())
            self.assertIn(layout['contents'], nsoup.contents())