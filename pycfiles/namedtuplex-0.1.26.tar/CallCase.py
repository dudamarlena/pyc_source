# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/namedtuplex/components/namedtuplex/tests/namedtuplex_tests/namedtuple_reference_comparison/Case030/CallCase.py
# Compiled at: 2019-06-19 10:56:08
from __future__ import absolute_import
__author__ = 'Arno-Can Uestuensoez'
__license__ = 'Artistic-License-2.0 + Forced-Fairplay-Constraints'
__copyright__ = 'Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
__version__ = '0.0.1'
__uuid__ = 'e3590f7b-2a97-4091-9534-d203d49a92ad'
__docformat__ = 'restructuredtext en'
import unittest, collections
from namedtupledefs import namedtuple

class CallUnits(unittest.TestCase):

    def testCase000(self):
        MyClass_collections = collections.namedtuple('MyClassABC', ('f0', 'f1', 'f2'))

        class MyClass_collections2(MyClass_collections):
            pass

        MyClass_nametuple = namedtuple('MyClassABC', ('f0', 'f1', 'f2'))

        class MyClass_nametuple2(MyClass_nametuple):
            pass

        inst_collections = MyClass_collections2(1, 2, 3)
        inst_namedtuple = MyClass_nametuple2(1, 2, 3)
        x0 = inst_collections.__eq__(inst_namedtuple)
        self.assertTrue(x0)
        x1 = inst_collections == inst_namedtuple
        self.assertTrue(x1)
        x2 = tuple(inst_collections) == inst_namedtuple
        self.assertTrue(x2)
        x3 = tuple(inst_collections) == tuple(inst_namedtuple)
        self.assertTrue(x3)
        x4 = inst_collections == tuple(inst_namedtuple)
        self.assertTrue(x4)
        y0 = inst_namedtuple == inst_collections
        self.assertTrue(y0)
        self.assertEqual(inst_collections, inst_namedtuple)


if __name__ == '__main__':
    unittest.main()