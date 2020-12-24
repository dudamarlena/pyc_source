# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_column.py
# Compiled at: 2015-09-22 05:47:42
from __future__ import unicode_literals
from nose.tools import ok_, eq_
from sqlalchemy import Integer, Numeric, String, Date, DateTime, Time, Text, Float, Boolean, LargeBinary
from dmsa.makers import make_column

def test_types():
    fields_json = [{b'type': b'integer', b'name': b'integer'}, {b'type': b'number', b'name': b'number', b'precision': 10, b'scale': 5}, {b'type': b'decimal', b'name': b'decimal', b'precision': 10, b'scale': 5}, {b'type': b'float', b'name': b'float'}, {b'type': b'string', b'name': b'string', b'length': 128}, {b'type': b'date', b'name': b'date'}, {b'type': b'datetime', b'name': b'datetime'}, {b'type': b'timestamp', b'name': b'timestamp'}, {b'type': b'time', b'name': b'time'}, {b'type': b'text', b'name': b'text'}, {b'type': b'clob', b'name': b'clob'}, {b'type': b'boolean', b'name': b'boolean'}, {b'type': b'blob', b'name': b'blob'}]
    field_types = [
     Integer,
     Numeric,
     Numeric,
     Float,
     String,
     Date,
     DateTime,
     DateTime,
     Time,
     Text,
     Text,
     Boolean,
     LargeBinary]
    for i in range(len(fields_json)):
        field = make_column(fields_json[i])
        yield (check_field_type, field, field_types[i])


def check_field_type(field, field_type):
    assert isinstance(field.type, field_type)


def test_doc():
    field_json = {b'type': b'string', b'name': b'string', b'description': b'test string field'}
    field = make_column(field_json)
    eq_(field.doc, b'test string field')


def test_default():
    field_json = {b'type': b'string', b'name': b'string', b'default': b'testing'}
    field = make_column(field_json)
    eq_(field.default.arg, b'testing')
    eq_(field.server_default.arg, b'testing')


def test_nullable():
    field_json = {b'type': b'string', b'name': b'string'}
    field = make_column(field_json, True)
    ok_(not field.nullable)


def test_length():
    field_json = {b'type': b'string', b'name': b'string', b'length': 128}
    field = make_column(field_json)
    eq_(field.type.length, 128)


def test_length_default():
    field_json = {b'type': b'string', b'name': b'string'}
    field = make_column(field_json)
    eq_(field.type.length, 256)


def test_numeric_precision_scale():
    field_json = {b'type': b'decimal', b'name': b'decimal', b'precision': 50, b'scale': 15}
    field = make_column(field_json)
    eq_(field.type.precision, 50)
    eq_(field.type.scale, 15)


def test_numeric_precision_scale_defaults():
    field_json = {b'type': b'decimal', b'name': b'decimal'}
    field = make_column(field_json)
    eq_(field.type.precision, 20)
    eq_(field.type.scale, 5)