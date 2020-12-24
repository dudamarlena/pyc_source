# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/runeh/development/anyjson/tests/test_implementations.py
# Compiled at: 2012-06-21 18:59:59
from nose.tools import assert_raises
import anyjson
modnames = [ e[0] for e in anyjson._modules ]

def test_default_serialization():
    assert anyjson.dumps([1, 2, 3]).replace(' ', '') == '[1,2,3]'
    assert anyjson.serialize([1, 2, 3]).replace(' ', '') == '[1,2,3]'


def test_default_deserialization():
    assert anyjson.loads('[1,2,3]') == [1, 2, 3]
    assert anyjson.deserialize('[1,2,3]') == [1, 2, 3]


def test_forced_serialization():
    for name in modnames:
        try:
            anyjson.force_implementation(name)
        except ImportError:
            continue

        assert anyjson.dumps([1, 2, 3]).replace(' ', '') == '[1,2,3]'
        assert anyjson.serialize([1, 2, 3]).replace(' ', '') == '[1,2,3]'


def test_forced_deserialization():
    for name in modnames:
        try:
            anyjson.force_implementation(name)
        except ImportError:
            continue

        assert anyjson.loads('[1,2,3]') == [1, 2, 3]
        assert anyjson.deserialize('[1,2,3]') == [1, 2, 3]


def test_exceptions():
    for name in modnames:
        try:
            anyjson.force_implementation(name)
        except ImportError:
            continue

        assert_raises(TypeError, anyjson.dumps, [object()])
        assert_raises(TypeError, anyjson.serialize, [object()])
        assert_raises(ValueError, anyjson.loads, '[')
        assert_raises(ValueError, anyjson.deserialize, '[')


def test_json_loads_unicode():
    try:
        anyjson.force_implementation('json')
    except ImportError:
        return

    assert 'foo' in anyjson.loads('{"foo": "bar"}')