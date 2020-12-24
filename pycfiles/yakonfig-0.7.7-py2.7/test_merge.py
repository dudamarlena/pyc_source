# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yakonfig/tests/test_merge.py
# Compiled at: 2015-07-07 22:00:14
"""Unit tests for yakonfig.merge.

.. This software is released under an MIT/X11 open source license.
   Copyright 2014-2015 Diffeo, Inc.

"""
from __future__ import absolute_import
import yakonfig.merge

def test_overlay():
    oc = yakonfig.merge.overlay_config
    assert oc('foo', 'bar') == 'bar'
    assert oc({'k': 'v'}, 'bar') == 'bar'
    assert oc('foo', {'k': 'v'}) == {'k': 'v'}
    assert oc({'a': 'a'}, {}) == {'a': 'a'}
    assert oc({'a': 'a'}, {'a': None}) == {}
    assert oc({'a': 'a'}, {'a': 'b'}) == {'a': 'b'}
    assert oc({'a': 'a'}, {'b': 'b'}) == {'a': 'a', 'b': 'b'}
    assert oc({'a': 'x', 'b': 'y'}, {}) == {'a': 'x', 'b': 'y'}
    assert oc({'a': 'x', 'b': 'y'}, {'a': None}) == {'b': 'y'}
    assert oc({'a': 'x', 'b': 'y'}, {'b': 'foo', 'c': 'bar'}) == {'a': 'x', 'b': 'foo', 'c': 'bar'}
    assert oc({'a': {'1': 'one'}}, {'a': {'2': 'two'}}) == {'a': {'1': 'one', '2': 'two'}}
    assert oc({'a': {'1': 'one'}}, {'a': {'1': None}}) == {'a': {}}
    assert oc({'a': {'1': 'one'}}, {'a': {'2': 'two'}, 'b': {'3': 'three'}}) == {'a': {'1': 'one', '2': 'two'}, 'b': {'3': 'three'}}
    assert oc({'a': None}, {}) == {'a': None}
    assert oc({'a': None}, {'a': 1}) == {'a': 1}
    assert oc({'a': None}, {'a': None}) == {'a': None}
    return


def test_diff():
    dc = yakonfig.merge.diff_config
    assert dc('foo', 'bar') == 'bar'
    assert dc({'k': 'v'}, 'bar') == 'bar'
    assert dc('foo', {'k': 'v'}) == {'k': 'v'}
    assert dc({'a': 'a'}, {'a': 'a'}) == {}
    assert dc({'a': 'a'}, {}) == {'a': None}
    assert dc({'a': 'a'}, {'a': 'b'}) == {'a': 'b'}
    assert dc({'a': 'a'}, {'a': 'a', 'b': 'b'}) == {'b': 'b'}
    assert dc({'a': 'x', 'b': 'y'}, {'a': 'x', 'b': 'y'}) == {}
    assert dc({'a': 'x', 'b': 'y'}, {'b': 'y'}) == {'a': None}
    assert dc({'a': 'x', 'b': 'y'}, {'a': 'x', 'b': 'foo', 'c': 'bar'}) == {'b': 'foo', 'c': 'bar'}
    assert dc({'a': {'1': 'one'}}, {'a': {'1': 'one', '2': 'two'}}) == {'a': {'2': 'two'}}
    assert dc({'a': {'1': 'one'}}, {'a': {}}) == {'a': {'1': None}}
    assert dc({'a': {'1': 'one'}}, {'a': {'1': 'one', '2': 'two'}, 'b': {'3': 'three'}}) == {'a': {'2': 'two'}, 'b': {'3': 'three'}}
    return