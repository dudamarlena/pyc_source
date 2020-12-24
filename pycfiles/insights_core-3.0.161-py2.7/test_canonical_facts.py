# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_canonical_facts.py
# Compiled at: 2019-05-16 13:41:33
from insights.util.canonical_facts import _filter_falsy

def test_identity():
    assert {'foo': 'bar'} == _filter_falsy({'foo': 'bar'})


def test_drops_none():
    assert {'foo': 'bar'} == _filter_falsy({'foo': 'bar', 'baz': None})
    return


def test_drops_empty_list():
    assert {'foo': 'bar'} == _filter_falsy({'foo': 'bar', 'baz': []})