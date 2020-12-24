# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_utils/test_paginator.py
# Compiled at: 2013-07-03 05:00:55
from unittest import TestCase
from nose import tools
from ella.utils.pagination import FirstPagePaginator
OBJECTS = [
 '1', '2', '3', '4', '5']

class TestPaginator(TestCase):

    def test_diffrerent_first_page(self):
        p = FirstPagePaginator(OBJECTS, first_page_count=1, per_page=2)
        tools.assert_equals(p.page(1).object_list, ['1'])

    def test_other_pages(self):
        p = FirstPagePaginator(OBJECTS, first_page_count=1, per_page=2)
        tools.assert_equals(p.page(2).object_list, ['2', '3'])
        tools.assert_equals(p.page(3).object_list, ['4', '5'])

    def test_all_pages_same(self):
        p = FirstPagePaginator(OBJECTS, per_page=2)
        tools.assert_equals(p.page(1).object_list, ['1', '2'])
        tools.assert_equals(p.page(2).object_list, ['3', '4'])