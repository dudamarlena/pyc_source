# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_model.py
# Compiled at: 2015-09-11 15:47:35
from __future__ import unicode_literals
from sqlalchemy import MetaData
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint
from nose.tools import eq_, ok_
from dmsa.makers import make_model
model_json = {b'schema': {b'constraints': {b'foreign_keys': [
                                                {b'source_table': b'test_table_1', b'source_field': b'integer', 
                                                   b'target_table': b'test_table_2', 
                                                   b'target_field': b'integer'}], 
                                b'not_null': [{b'table': b'test_table_1', b'field': b'string'}], b'uniques': [{b'table': b'test_table_2', b'fields': [b'integer']}], b'primary_keys': [{b'table': b'test_table_1', b'fields': [b'pk']}]}, 
               b'indexes': [{b'table': b'test_table_2', b'fields': [b'string']}]}, 
   b'tables': [
             {b'name': b'test_table_1', b'fields': [
                          {b'type': b'integer', b'name': b'pk'},
                          {b'type': b'integer', b'name': b'integer'},
                          {b'type': b'string', b'name': b'string', 
                             b'length': 0}]},
             {b'name': b'test_table_2', b'fields': [
                          {b'type': b'integer', b'name': b'integer'},
                          {b'type': b'string', b'name': b'string', 
                             b'length': 0}]}]}

def test_pk():
    metadata = MetaData()
    metadata = make_model(model_json, metadata)
    tbl1 = metadata.tables[b'test_table_1']
    ok_(b'pk' in tbl1.primary_key.columns)


def test_unique():
    metadata = MetaData()
    metadata = make_model(model_json, metadata)
    tbl2 = metadata.tables[b'test_table_2']
    for con in tbl2.constraints:
        if isinstance(con, UniqueConstraint):
            ok_(b'integer' in con.columns)
            break
    else:
        raise AssertionError(b'UniqueConstraint not found.')


def test_not_null():
    metadata = MetaData()
    metadata = make_model(model_json, metadata)
    tbl1 = metadata.tables[b'test_table_1']
    col = tbl1.columns[b'string']
    ok_(not col.nullable)


def test_index():
    metadata = MetaData()
    metadata = make_model(model_json, metadata)
    tbl2 = metadata.tables[b'test_table_2']
    for idx in tbl2.indexes:
        ok_(b'string' in idx.columns)
        break
    else:
        raise AssertionError(b'Index not found.')


def test_foreign_key():
    metadata = MetaData()
    metadata = make_model(model_json, metadata)
    tbl1 = metadata.tables[b'test_table_1']
    for con in tbl1.constraints:
        if isinstance(con, ForeignKeyConstraint):
            ok_(b'integer' in con.columns)
            eq_(list(con.columns[b'integer'].foreign_keys)[0].target_fullname, b'test_table_2.integer')
            break
    else:
        raise AssertionError(b'ForeignKeyConstraint not found.')