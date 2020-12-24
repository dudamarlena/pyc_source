# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/testsuite/dotdict.py
# Compiled at: 2013-03-16 04:04:43
import unittest
from frame.dotdict import DotDict

class TestDotDict(unittest.TestCase):

    def setUp(self):
        self.data = DotDict({'name': {'first': 'Bob', 'last': 'Builder'}, 'email': 'bob@builder.com'})

    def test_assignment(self):
        self.data.name.first = 'Bobbert'
        assert self.data.name.first == self.data['name']['first']