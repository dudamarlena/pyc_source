# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/tests/general.py
# Compiled at: 2007-12-02 16:26:56
import unittest

class GeneralTest(unittest.TestCase):
    __module__ = __name__

    def testGeneral(self):
        self.assertEquals(1, 1)

    def testSomething(self):
        self.assertEquals(2, 2)

    def testSomethingOther(self):
        self.assertEquals(3, 3)


class GeneralTest2(unittest.TestCase):
    __module__ = __name__

    def testGeneral(self):
        self.assertEquals(1, 1)