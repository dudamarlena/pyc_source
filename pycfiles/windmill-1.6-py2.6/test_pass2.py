# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_pass2.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
import simplejson as json
JSON = '\n[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]]\n'

class TestPass2(TestCase):

    def test_parse(self):
        res = json.loads(JSON)
        out = json.dumps(res)
        self.assertEquals(res, json.loads(out))