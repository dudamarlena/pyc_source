# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbojson\tests\test_jsonify.py
# Compiled at: 2011-08-07 13:53:57
from datetime import date, datetime
from decimal import Decimal
from turbojson.jsonify import jsonify, encode, encode_iter

class Foo(object):
    __module__ = __name__

    def __init__(self, bar):
        self.bar = bar


class Bar(object):
    __module__ = __name__

    def __init__(self, bar):
        self.bar = bar

    def __json__(self):
        return 'bar-%s' % self.bar


class Baz(object):
    __module__ = __name__


@jsonify.when('isinstance(obj, Foo)')
def jsonify_foo(obj):
    return 'foo-%s' % obj.bar


def test_none():
    assert encode(None) == 'null'
    return


def test_bool():
    assert encode(True) == 'true'
    assert encode(False) == 'false'


def test_str():
    assert encode('bla') == '"bla"'


def test_unicode():
    assert encode('bla') == '"bla"'


def test_int():
    assert encode(42) == '42'


def test_long():
    assert encode(424242424242424242424242) == '424242424242424242424242'


def test_float():
    assert encode(1234.5) == '1234.5'


def test_list():
    d = [
     'a', 1, 'b', 2]
    encoded = encode(d)
    assert encoded == '["a", 1, "b", 2]'


def test_list_iter():
    d = range(3)
    encoded = encode_iter(d)
    assert ('').join(encode_iter(d)) == encode(d)


def test_dictionary():
    d = {'a': 1, 'b': 2}
    encoded = encode(d)
    assert encoded == '{"a": 1, "b": 2}'


def test_tuple():
    assert encode((1, 2, 3)) == '[1, 2, 3]'


def test_set():
    assert encode(set([1, 2, 3])) == '[1, 2, 3]'
    assert encode(frozenset([1, 2, 3])) == '[1, 2, 3]'


def test_decimal():
    assert encode(Decimal('2.5') == '2.5')


def test_datetime():
    assert encode(date(1917, 10, 25)) == '"1917-10-25"'
    assert encode(datetime(1917, 10, 25, 21, 45)) == '"1917-10-25 21:45:00"'


def test_specific_json():
    a = Foo('baz')
    encoded = encode(a)
    assert encoded == '"foo-baz"'


def test_specific_in_list():
    a = Foo('baz')
    d = [a]
    encoded = encode(d)
    assert encoded == '["foo-baz"]'


def test_specific_in_dict():
    a = Foo('baz')
    d = {'a': a}
    encoded = encode(d)
    assert encoded == '{"a": "foo-baz"}'


def test_no_specific_json():
    b = Baz()
    try:
        encoded = encode(b)
    except Exception, e:
        encoded = e.__class__.__name__

    assert encoded == 'NoApplicableMethods'


def test_exlicit_json():
    b = Bar('bq')
    encoded = encode(b)
    assert encoded == '"bar-bq"'


def test_exlicit_json_in_list():
    b = Bar('bq')
    d = [b]
    encoded = encode(d)
    assert encoded == '["bar-bq"]'


def test_exlicit_json_in_dict():
    b = Bar('bq')
    d = {'b': b}
    encoded = encode(d)
    assert encoded == '{"b": "bar-bq"}'