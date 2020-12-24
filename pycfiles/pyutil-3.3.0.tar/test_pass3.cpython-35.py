# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_pass3.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 565 bytes
from unittest import TestCase
from pyutil import jsonutil as json
JSON = '\n{\n    "JSON Test Pattern pass3": {\n        "The outermost value": "must be an object or array.",\n        "In this test": "It is an object."\n    }\n}\n'

class TestPass3(TestCase):

    def test_parse(self):
        res = json.loads(JSON)
        out = json.dumps(res)
        self.assertEqual(res, json.loads(out))