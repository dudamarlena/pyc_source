# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tests/utils/test_table_meta.py
# Compiled at: 2018-04-02 06:43:38
# Size of source mod 2**32: 2134 bytes
from trane.utils.table_meta import TableMeta as TM

def test_table_meta_set_get():
    meta = TM({'tables': [
                {'fields': [{'name': 'col1',  'type': TM.TYPE_IDENTIFIER},
                            {'name': 'col2',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                             'subtype': TM.TYPE_FLOAT}]}]})
    assert meta.get_type('col1') == TM.TYPE_IDENTIFIER
    assert meta.get_type('col2') == TM.TYPE_FLOAT
    meta.set_type('col2', TM.TYPE_TEXT)
    assert meta.get_type('col1') == TM.TYPE_IDENTIFIER
    assert meta.get_type('col2') == TM.TYPE_TEXT


def test_table_meta_get_columns():
    meta = TM({'tables': [
                {'fields': [{'name': 'col1',  'type': TM.TYPE_IDENTIFIER},
                            {'name': 'col2',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                             'subtype': TM.TYPE_FLOAT}]}]})
    columns = meta.get_columns()
    assert len(columns) == 2
    assert 'col1' in columns and 'col2' in columns


def test_table_meta_copy():
    meta = TM({'tables': [
                {'fields': [{'name': 'col1',  'type': TM.TYPE_IDENTIFIER},
                            {'name': 'col2',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                             'subtype': TM.TYPE_FLOAT}]}]})
    meta2 = meta.copy()
    meta2.set_type('col2', TM.TYPE_TIME)
    meta.set_type('col1', TM.TYPE_BOOL)
    assert meta.get_type('col1') == TM.TYPE_BOOL
    assert meta.get_type('col2') == TM.TYPE_FLOAT
    assert meta2.get_type('col1') == TM.TYPE_IDENTIFIER
    assert meta2.get_type('col2') == TM.TYPE_TIME


def test_table_meta_load_save():
    meta = TM({'tables': [
                {'fields': [{'name': 'col1',  'type': TM.TYPE_IDENTIFIER},
                            {'name': 'col2',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                             'subtype': TM.TYPE_FLOAT}]}]})
    meta_json = meta.to_json()
    assert type(meta_json) == str
    meta2 = TM.from_json(meta_json)
    assert meta2.get_type('col1') == TM.TYPE_IDENTIFIER
    assert meta2.get_type('col2') == TM.TYPE_FLOAT