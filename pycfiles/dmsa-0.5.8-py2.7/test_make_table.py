# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_table.py
# Compiled at: 2015-09-11 15:47:35
from __future__ import unicode_literals
from nose.tools import eq_, ok_
from sqlalchemy import MetaData
from dmsa.makers import make_table

def test_name():
    table_json = {b'name': b'test_table'}
    metadata = MetaData()
    table = make_table(table_json, metadata, [])
    eq_(table.name, b'test_table')


def test_metadata():
    table_json = {b'name': b'test_table'}
    metadata = MetaData()
    table = make_table(table_json, metadata, [])
    eq_(metadata.tables[table.name], table)


def test_fields():
    table_json = {b'name': b'test_table', b'fields': [
                 {b'type': b'integer', b'name': b'integer'}]}
    metadata = MetaData()
    table = make_table(table_json, metadata, [])
    ok_(b'integer' in table.columns)


def test_not_null():
    table_json = {b'name': b'test_table', b'fields': [
                 {b'type': b'integer', b'name': b'integer'}]}
    not_nulls = [{b'table': b'test_table', b'field': b'integer'}]
    metadata = MetaData()
    table = make_table(table_json, metadata, not_nulls)
    ok_(not table.columns[b'integer'].nullable)