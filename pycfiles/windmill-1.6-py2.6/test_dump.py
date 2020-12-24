# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_dump.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
from cStringIO import StringIO
import simplejson as json

class TestDump(TestCase):

    def test_dump(self):
        sio = StringIO()
        json.dump({}, sio)
        self.assertEquals(sio.getvalue(), '{}')

    def test_dumps(self):
        self.assertEquals(json.dumps({}), '{}')

    def test_encode_truefalse(self):
        self.assertEquals(json.dumps({True: False, False: True}, sort_keys=True), '{"false": true, "true": false}')
        self.assertEquals(json.dumps({2: 3.0, 4.0: 5, False: 1, 6: True, '7': 0}, sort_keys=True), '{"false": 1, "2": 3.0, "4.0": 5, "6": true, "7": 0}')