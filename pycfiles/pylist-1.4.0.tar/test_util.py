# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylispng/util/test/test_util.py
# Compiled at: 2008-11-11 00:23:38
import unittest
from pylispng import util

class UtilTestCase(unittest.TestCase):
    """

    """
    __module__ = __name__

    def test_arity(self):
        """

        """
        funcs = [
         'abs', '+', 'a']
        arities = [1, 2, 0]
        for (func, expected) in zip(funcs, arities):
            arity = util.getArity(func)
            self.assertEquals(arity, expected)

    def test_dynamicList(self):
        """

        """
        dl = util.DynamicList()
        self.assertEquals(len(dl), 0)
        dl[0] = 'apple'
        self.assertEquals(len(dl), 1)
        self.assertEquals(dl[0], 'apple')
        dl[11] = 'orange'
        self.assertEquals(len(dl), 12)
        self.assertEquals(dl[11], 'orange')
        self.assertEquals(dl[1], None)
        self.assertEquals(dl[10], None)
        return