# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Documents/0x01.Source/twnews/build/lib/twnews/tests/soup/test_soup_chinatimes.py
# Compiled at: 2019-08-13 05:08:43
# Size of source mod 2**32: 1475 bytes
"""
中時電子報分解測試
"""
import unittest, twnews.common
from twnews.soup import NewsSoup

class TestChinatimes(unittest.TestCase):
    __doc__ = '\n    中時電子報分解測試\n    '

    def setUp(self):
        self.url = 'https://www.chinatimes.com/realtimenews/20180916001767-260402'
        self.dtf = '%Y-%m-%d %H:%M:%S'

    def test_01_sample(self):
        """
        測試中時電子報樣本
        """
        pkgdir = twnews.common.get_package_dir()
        nsoup = NewsSoup(pkgdir + '/samples/chinatimes.html.gz')
        self.assertEqual('chinatimes', nsoup.channel)
        self.assertIn('悲慟！北市士林年邁母子 住處上吊自殺身亡', nsoup.title())
        self.assertEqual('2018-09-16 15:31:00', nsoup.date().strftime(self.dtf))
        self.assertEqual('謝明俊', nsoup.author())
        self.assertIn('北市士林區葫蘆街一處民宅', nsoup.contents())

    def test_02_mobile(self):
        """
        測試中時電子報行動版
        """
        nsoup = NewsSoup((self.url), refresh=True)
        self.assertEqual('chinatimes', nsoup.channel)
        self.assertIn('悲慟！北市士林年邁母子 住處上吊自殺身亡', nsoup.title())
        self.assertEqual('2018-09-16 15:31:00', nsoup.date().strftime(self.dtf))
        self.assertEqual('謝明俊', nsoup.author())
        self.assertIn('北市士林區葫蘆街一處民宅', nsoup.contents())