# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\adv\test_messageloop.py
# Compiled at: 2016-03-08 18:42:10
import unittest2 as unittest
from b3.plugins.adv import MessageLoop

class Test_MessageLoop(unittest.TestCase):

    def test_empty(self):
        ml = MessageLoop()
        self.assertEqual([], ml.items)
        self.assertEqual(None, ml.getnext())
        return

    def test_one_element(self):
        ml = MessageLoop()
        ml.items = ['f00']
        self.assertEqual('f00', ml.getnext())
        self.assertEqual('f00', ml.getnext())

    def test_three_elements(self):
        ml = MessageLoop()
        ml.items = ['f001', 'f002', 'f003']
        self.assertEqual('f001', ml.getnext())
        self.assertEqual('f002', ml.getnext())
        self.assertEqual('f003', ml.getnext())
        self.assertEqual('f001', ml.getnext())
        self.assertEqual('f002', ml.getnext())
        self.assertEqual('f003', ml.getnext())

    def test_put(self):
        ml = MessageLoop()
        self.assertEqual([], ml.items)
        ml.put('bar')
        self.assertEqual(['bar'], ml.items)

    def test_getitem(self):
        ml = MessageLoop()
        ml.items = ['f00']
        self.assertEqual('f00', ml.getitem(0))
        self.assertEqual(None, ml.getitem(1))
        return

    def test_remove(self):
        ml = MessageLoop()
        ml.items = ['f00', 'bar']
        self.assertEqual('f00', ml.getitem(0))
        ml.remove(0)
        self.assertEqual(['bar'], ml.items)
        self.assertEqual('bar', ml.getitem(0))

    def test_clear(self):
        ml = MessageLoop()
        ml.items = ['f00', 'bar']
        ml.clear()
        self.assertEqual([], ml.items)