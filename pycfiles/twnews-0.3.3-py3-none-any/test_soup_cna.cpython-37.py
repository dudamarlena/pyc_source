# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/tests/soup/test_soup_cna.py
# Compiled at: 2019-08-13 05:08:48
# Size of source mod 2**32: 1428 bytes
"""
中央社分解測試
"""
import unittest, twnews.common
from twnews.soup import NewsSoup

class TestCna(unittest.TestCase):
    __doc__ = '\n    中央社分解測試\n    '

    def setUp(self):
        self.url = 'https://www.cna.com.tw/news/asoc/201810170077.aspx'
        self.dtf = '%Y-%m-%d %H:%M:%S'

    def test_01_sample(self):
        """
        測試中央社樣本
        """
        pkgdir = twnews.common.get_package_dir()
        nsoup = NewsSoup(pkgdir + '/samples/cna.html.gz')
        self.assertEqual('cna', nsoup.channel)
        self.assertIn('平鎮輪胎行惡火  疏散7人1女命喪', nsoup.title())
        self.assertEqual('2016-03-19 10:48:00', nsoup.date().strftime(self.dtf))
        self.assertEqual('邱俊欽', nsoup.author())
        self.assertIn('桃園市平鎮區一家輪胎行', nsoup.contents())

    def test_02_mobile(self):
        """
        測試中央社行動版
        """
        nsoup = NewsSoup((self.url), refresh=True)
        self.assertEqual('cna', nsoup.channel)
        self.assertIn('前女友輕生  前男友到殯儀館砍現任還開槍', nsoup.title())
        self.assertEqual('2018-10-17 14:06:00', nsoup.date().strftime(self.dtf))
        self.assertEqual('黃國芳', nsoup.author())
        self.assertIn('民主進步黨籍嘉義市議員王美惠上午到殯儀館參加公祭', nsoup.contents())