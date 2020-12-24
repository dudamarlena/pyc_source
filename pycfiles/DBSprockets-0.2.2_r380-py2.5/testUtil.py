# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testUtil.py
# Compiled at: 2008-06-30 11:43:30
from dbsprockets.util import MultiDict
from nose.tools import eq_

class testMultiDict:

    def setup(self):
        self.m = MultiDict()
        self.m['a'] = 1
        self.m['b'] = 2
        self.m['a'] = 3

    def testCreate(self):
        pass

    def testIterItems(self):
        actual = [ (key, value) for (key, value) in self.m.iteritems() ]
        eq_(actual, [('a', 1), ('a', 3), ('b', 2)])