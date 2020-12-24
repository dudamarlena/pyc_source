# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_selectBuilder.py
# Compiled at: 2016-06-15 12:04:46
# Size of source mod 2**32: 1887 bytes
from unittest import TestCase
from sqlstring.sql_builder import SelectBuilder

class TestSelectBuilder(TestCase):

    def setUp(self):
        pass

    def test_from_table(self):
        builder = SelectBuilder()
        r = builder.from_table('address').get_query_string()
        self.assertEqual(len(r), 22)

    def test_column(self):
        builder = SelectBuilder()
        builder.from_table('address').column(['city', 'state_code'])
        r = builder.get_query_string()
        self.assertEqual(len(r), 37)

    def test_group_by(self):
        builder = SelectBuilder()
        builder.from_table('address').group_by(['state_code', 'city'])
        r = builder.get_query_string()
        self.assertEqual(len(r), 48)

    def test_order_by(self):
        builder = SelectBuilder()
        builder.from_table('address').order_by(['state_code', 'city'], 'DESC')
        r = builder.get_query_string()
        self.assertEqual(len(r), 58)

    def test_limit(self):
        builder = SelectBuilder()
        r = builder.from_table('address').limit(100).offset(200).get_query_string()
        self.assertEqual(len(r), 43)

    def test_offset(self):
        builder = SelectBuilder()
        r = builder.from_table('address').limit(100).offset(200).get_query_string()
        self.assertEqual(len(r), 43)

    def test_distinct(self):
        builder = SelectBuilder()
        r = builder.from_table('address').distinct().get_query_string()
        self.assertEqual(len(r), 31)

    def test_join_table(self):
        builder = SelectBuilder()
        builder.from_table('address').join_table('contact')
        builder.where('address.state_code', '=', ' contact.state_code ')
        r = builder.get_query_string()
        self.assertEqual(len(r), 87)

    def test_get_query_string(self):
        pass