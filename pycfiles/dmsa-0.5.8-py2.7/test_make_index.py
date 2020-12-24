# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_index.py
# Compiled at: 2015-09-11 15:47:35
from __future__ import unicode_literals
from dmsa.makers import make_index
from nose.tools import eq_

def test_name():
    index_json = {b'name': b'test_index', b'fields': [b'id']}
    index = make_index(index_json)
    eq_(index.name, b'test_index')


def test_fields():
    index_json = {b'name': b'test_index', b'fields': [b'id']}
    index = make_index(index_json)
    eq_(index.expressions, ('id', ))