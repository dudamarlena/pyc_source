# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeb/code/git/WeatherAlerts/tests/test_feed.py
# Compiled at: 2017-03-27 21:33:56
# Size of source mod 2**32: 398 bytes
import os, sys
sys.path.insert(0, os.path.abspath('..'))
import unittest
from weatheralerts.feed import AlertsFeed

class Test_Feed(unittest.TestCase):

    def setUp(self):
        self.cf = AlertsFeed(maxage=5)

    def test_refesh(self):
        self.cf.raw_cap(refresh=True)
        self.cf.raw_cap(refresh=False)


if __name__ == '__main__':
    unittest.main()