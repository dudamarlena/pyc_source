# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_insertBuilder.py
# Compiled at: 2016-06-15 12:04:46
# Size of source mod 2**32: 475 bytes
from unittest import TestCase
from sqlstring.sql_builder import InsertBuilder

class TestInsertBuilder(TestCase):

    def setUp(self):
        pass

    def test_into_table(self):
        builder = InsertBuilder()
        builder.into_table('address').column(['city', 'state_code'])
        r = builder.get_query_string()
        self.assertEqual(len(r), 67)

    def test_column(self):
        pass

    def test_get_query_string(self):
        pass