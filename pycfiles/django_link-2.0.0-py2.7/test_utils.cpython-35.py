# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/tests/test_utils.py
# Compiled at: 2017-07-06 07:47:29
# Size of source mod 2**32: 268 bytes
from django.test import TestCase
from link import utils

class UtilsTestCase(TestCase):

    def test_get_view_names(self):
        self.assertEqual(utils.get_view_names(), [
         'link-1', 'link-2', 'link:link-list', 'link:link-detail'])