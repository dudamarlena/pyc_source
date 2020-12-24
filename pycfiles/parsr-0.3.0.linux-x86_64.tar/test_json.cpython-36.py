# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_json.py
# Compiled at: 2019-05-28 16:55:06
# Size of source mod 2**32: 2947 bytes
import json
from parsr.examples.json_parser import TRUE, FALSE, NULL, JsonArray, JsonObject, JsonValue
DATA0 = '\n{\n    "name": "Adventure Lookup"\n}\n'.strip()
DATA1 = '\n{\n    "name": "Adventure Lookup",\n    "icons": [\n        {\n            "src": "/android-chrome-192x192.png",\n            "sizes": "192x192",\n            "type": "image/png"\n        },\n        {\n            "src": "/android-chrome-512x512.png",\n            "sizes": "512x512",\n            "type": "image/png"\n        }\n    ],\n    "theme_color": "#ffffff",\n    "background_color": "#ffffff",\n    "display": "standalone"\n}\n'.strip()
DATA2 = '\n{\n  "meta": {\n    "version": "0.6.0"\n  },\n  "GROUPS": {\n    "c-development": {\n      "grp_types": 0,\n      "ui_name": "C Development Tools and Libraries",\n      "name": "C Development Tools and Libraries",\n      "full_list": [\n        "valgrind",\n        "automake",\n        "indent",\n        "autoconf",\n        "ltrace",\n        "bison",\n        "ccache",\n        "gdb",\n        "strace",\n        "elfutils",\n        "byacc",\n        "oprofile",\n        "gcc-c++",\n        "pkgconfig",\n        "binutils",\n        "gcc",\n        "libtool",\n        "cscope",\n        "ctags",\n        "flex",\n        "glibc-devel",\n        "make"\n      ],\n      "pkg_exclude": [],\n      "pkg_types": 6\n    }\n  },\n  "ENVIRONMENTS": {}\n}'.strip()

def test_true():
    assert TRUE('true') is True


def test_false():
    assert FALSE('false') is False


def test_null():
    assert NULL('null') is None


def test_json_value_number():
    assert JsonValue('123') == 123


def test_json_value_string():
    assert JsonValue('"key"') == 'key'


def test_json_empty_array():
    assert JsonArray('[]') == []


def test_json_single_element_array():
    assert JsonArray("['key']") == ['key']


def test_json_multi_element_array():
    if not JsonArray('[1, 2, 3]') == [1, 2, 3]:
        raise AssertionError
    elif not JsonArray("['key', -3.4, 'thing']") == ['key', -3.4, 'thing']:
        raise AssertionError


def test_json_nested_array():
    if not JsonArray('[1, [4, 5], 3]') == [1, [4, 5], 3]:
        raise AssertionError
    elif not JsonArray("['key', [-3.4], 'thing']") == ['key', [-3.4], 'thing']:
        raise AssertionError


def test_json_empty_object():
    assert JsonObject('{}') == {}


def test_json_single_object():
    assert JsonObject('{"key": "value"}') == {'key': 'value'}


def test_json_multi_object():
    expected = {'key1':'value1', 
     'key2':15}
    assert JsonObject('{"key1": "value1", "key2": 15}') == expected


def test_json_nested_object():
    text = '{ "key1": ["value1", "value2"], "key2": {"num": 15, "num2": 17 }}'
    expected = {'key1':['value1', 'value2'],  'key2':{'num':15,  'num2':17}}
    assert JsonObject(text) == expected


def test_data0():
    expected = json.loads(DATA0)
    assert JsonValue(DATA0) == expected


def test_data1():
    expected = json.loads(DATA1)
    assert JsonValue(DATA1) == expected


def test_data2():
    expected = json.loads(DATA2)
    assert JsonValue(DATA2) == expected