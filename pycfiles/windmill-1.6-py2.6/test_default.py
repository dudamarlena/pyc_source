# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_default.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
import simplejson as json

class TestDefault(TestCase):

    def test_default(self):
        self.assertEquals(json.dumps(type, default=repr), json.dumps(repr(type)))