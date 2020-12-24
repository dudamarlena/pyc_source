# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/tests/fixture_magic/test_utils.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 718 bytes
from __future__ import absolute_import
import os, unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
from fixture_magic.utils import reorder_json, get_fields
__author__ = 'davedash'

class UtilsTestCase(unittest.TestCase):

    def test_reorder_json(self):
        """Test basic ordering of JSON/python object."""
        input_json = [
         {'model': 'f'}, {'model': 'x'}]
        expected = [{'model': 'x'}, {'model': 'f'}]
        self.assertEqual(expected, reorder_json(input_json, models=['x', 'f']))

    def test_get_fields(self):
        obj = lambda : None
        obj._meta = lambda : None
        obj._meta.fields = ['foo']
        self.assertEqual(['foo'], get_fields(obj))