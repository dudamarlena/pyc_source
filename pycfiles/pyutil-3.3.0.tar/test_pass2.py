# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_pass2.py
# Compiled at: 2019-06-26 11:58:00
from unittest import TestCase
from pyutil import jsonutil as json
JSON = '\n[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]]\n'

class TestPass2(TestCase):

    def test_parse(self):
        res = json.loads(JSON)
        out = json.dumps(res)
        self.assertEqual(res, json.loads(out))