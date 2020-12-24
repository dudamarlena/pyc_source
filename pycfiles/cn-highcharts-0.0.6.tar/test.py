# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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