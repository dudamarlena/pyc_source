# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_constraint.py
# Compiled at: 2015-09-11 15:47:35
from __future__ import unicode_literals
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint
from dmsa.makers import make_constraint
from nose.tools import eq_, ok_
CONSTRAINT_MAP = {b'primary_keys': PrimaryKeyConstraint, 
   b'foreign_keys': ForeignKeyConstraint, 
   b'uniques': UniqueConstraint}

def test_name():
    for con_type, con_class in CONSTRAINT_MAP.iteritems():
        if con_type == b'foreign_keys':
            con_json = {b'name': b'test_con', b'source_field': b'id', b'target_table': b'foo', b'target_field': b'bar'}
        else:
            con_json = {b'name': b'test_con', b'fields': [b'id']}
        constraint = make_constraint(con_type, con_json)
        yield (check_name, constraint, b'test_con')


def check_name(constraint, name):
    eq_(constraint.name, name)


def test_types():
    for con_type, con_class in CONSTRAINT_MAP.iteritems():
        if con_type == b'foreign_keys':
            con_json = {b'name': b'test_con', b'source_field': b'id', b'target_table': b'foo', b'target_field': b'bar'}
        else:
            con_json = {b'name': b'test_con', b'fields': [b'id']}
        constraint = make_constraint(con_type, con_json)
        assert isinstance(constraint, con_class)


def test_fields():
    for con_type, con_class in CONSTRAINT_MAP.iteritems():
        if con_type == b'foreign_keys':
            con_json = {b'name': b'test_con', b'source_field': b'id', b'target_table': b'foo', b'target_field': b'bar'}
        else:
            con_json = {b'name': b'test_con', b'fields': [b'id']}
        constraint = make_constraint(con_type, con_json)
        if con_type == b'foreign_keys':
            eq_(constraint.column_keys, [b'id'])
            eq_(constraint.elements[0].target_fullname, b'foo.bar')
        else:
            eq_(constraint._pending_colargs, [b'id'])


def test_foreign_key_use_alter():
    con_type = b'foreign_keys'
    con_json = {b'name': b'test_con', b'source_field': b'id', b'target_table': b'foo', 
       b'target_field': b'bar'}
    constraint = make_constraint(con_type, con_json)
    ok_(constraint.use_alter)