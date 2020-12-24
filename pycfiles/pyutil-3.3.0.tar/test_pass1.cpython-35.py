# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_pass1.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 1886 bytes
from unittest import TestCase
from pyutil import jsonutil as json
JSON = '\n[\n    "JSON Test Pattern pass1",\n    {"object with 1 member":["array with 1 element"]},\n    {},\n    [],\n    -42,\n    true,\n    false,\n    null,\n    {\n        "integer": 1234567890,\n        "real": -9876.543210,\n        "e": 0.123456789e-12,\n        "E": 1.234567890E+34,\n        "":  23456789012E666,\n        "zero": 0,\n        "one": 1,\n        "space": " ",\n        "quote": "\\"",\n        "backslash": "\\\\",\n        "controls": "\\b\\f\\n\\r\\t",\n        "slash": "/ & \\/",\n        "alpha": "abcdefghijklmnopqrstuvwyz",\n        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",\n        "digit": "0123456789",\n        "special": "`1~!@#$%^&*()_+-={\':[,]}|;.</>?",\n        "hex": "\\u0123\\u4567\\u89AB\\uCDEF\\uabcd\\uef4A",\n        "true": true,\n        "false": false,\n        "null": null,\n        "array":[  ],\n        "object":{  },\n        "address": "50 St. James Street",\n        "url": "http://www.JSON.org/",\n        "comment": "// /* <!-- --",\n        "# -- --> */": " ",\n        " s p a c e d " :[1,2 , 3\n\n,\n\n4 , 5        ,          6           ,7        ],\n        "compact": [1,2,3,4,5,6,7],\n        "jsontext": "{\\"object with 1 member\\":[\\"array with 1 element\\"]}",\n        "quotes": "&#34; \\u0022 %22 0x22 034 &#x22;",\n        "\\/\\\\\\"\\uCAFE\\uBABE\\uAB98\\uFCDE\\ubcda\\uef4A\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"\n: "A key can be any string"\n    },\n    0.5 ,98.6\n,\n99.44\n,\n\n1066\n\n\n,"rosebud"]\n'

class TestPass1(TestCase):

    def test_parse(self):
        res = json.loads(JSON)
        out = json.dumps(res)
        self.assertEqual(res, json.loads(out))
        self.assertTrue('2.3456789012E+676' in json.dumps(res, allow_nan=False))