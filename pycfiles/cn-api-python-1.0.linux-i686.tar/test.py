# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/cn_api_python/lib/python2.7/site-packages/cn_api_python/test.py
# Compiled at: 2012-02-06 15:16:43
import unittest
from api import CharityAPI

class TestApiCalls(unittest.TestCase):

    def setUp(self):
        self.api = CharityAPI()

    def test_categories(self):
        pass


if __name__ == '__main__':
    unittest.main()