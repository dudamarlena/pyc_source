# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/tests/test_items.py
# Compiled at: 2019-03-12 04:24:44
# Size of source mod 2**32: 905 bytes
from unittest import TestCase
import os
from fanart.items import LeafItem
from httpretty import httprettified, HTTPretty
from fanart.tests import LOCALDIR

class LeafItemTestCase(TestCase):

    def setUp(self):
        self.leaf = LeafItem(id=11977, likes=2, url='http://test.tv/50x50.txt')

    def test_str(self):
        self.assertEqual(str(self.leaf), 'http://test.tv/50x50.txt')

    @httprettified
    def test_content(self):
        with open(os.path.join(LOCALDIR, 'response/50x50.png'), 'rb') as (fp):
            body = fp.read()
        HTTPretty.register_uri((HTTPretty.GET),
          'http://test.tv/50x50.txt',
          body=body)
        self.assertEqual(self.leaf.content(), body)
        self.assertEqual(len(HTTPretty.latest_requests), 1)
        self.assertEqual(self.leaf.content(), body)
        self.assertEqual(len(HTTPretty.latest_requests), 1)