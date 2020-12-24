# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/africa/work/python/djnago-unisender/unisender/tests/cabinet_links.py
# Compiled at: 2014-07-23 09:14:57
import unittest, urllib
from unisender.unisender_urls import EMAIL_MESSAGES_LIST, EMAIL_MESSAGES_DETAIL, TAG_LIST, FIELD_LIST, CAMPAIGN_LIST, CAMPAIGN_DETAIL, SUBSCRIBELIST_LIST, SUBSCRIBELIST_DETAIL

class LinkOpenedTestCase(unittest.TestCase):

    def test_email_message_list(self):
        self.assertEquals(urllib.urlopen(EMAIL_MESSAGES_LIST).getcode(), 200)

    def test_email_message_detail(self):
        detail_url = EMAIL_MESSAGES_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)

    def test_tag_list(self):
        self.assertEquals(urllib.urlopen(TAG_LIST).getcode(), 200)

    def test_field_list(self):
        self.assertEquals(urllib.urlopen(FIELD_LIST).getcode(), 200)

    def test_campaign_list(self):
        self.assertEquals(urllib.urlopen(CAMPAIGN_LIST).getcode(), 200)

    def test_campaign_detail(self):
        detail_url = CAMPAIGN_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)

    def test_subscribe_list(self):
        self.assertEquals(urllib.urlopen(SUBSCRIBELIST_LIST).getcode(), 200)

    def test_subscribe_list_detail(self):
        detail_url = SUBSCRIBELIST_DETAIL + '1'
        self.assertEquals(urllib.urlopen(detail_url).getcode(), 200)