# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_updateBuilder.py
# Compiled at: 2016-06-15 12:04:46
# Size of source mod 2**32: 481 bytes
from unittest import TestCase
from sqlstring.sql_builder import UpdateBuilder

class TestUpdateBuilder(TestCase):

    def setUp(self):
        pass

    def test_update_table(self):
        builder = UpdateBuilder()
        builder.update_table('address').set('state_name', " 'California' ")
        r = builder.get_query_string()
        self.assertEqual(len(r), 46)

    def test_set(self):
        pass

    def test_get_query_string(self):
        pass