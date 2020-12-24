# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/test/testsymbol.py
# Compiled at: 2008-07-30 12:52:46
import testbase, unittest
from lpo.symbol import Symbol

class SymbolTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSymbol(self):
        sym = Symbol('one', 2)
        self.assertEquals(sym.name, 'one')
        self.assertEquals(sym.arity, 2)


def suite():
    alltests = unittest.TestLoader().loadTestsFromTestCase(SymbolTestCase)
    return alltests


if __name__ == '__main__':
    testbase.main(suite())