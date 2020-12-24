# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/support/util_sys.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 1, 2012\n\n@package: ally base\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nTesting for the  classes utility.\n'
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.support.util_sys import validateTypeFor
import unittest

class A:
    __slots__ = ('a', )

    def __init__(self):
        self.a = 1


class TestSys(unittest.TestCase):

    def testPropertyValidated(self):
        validateTypeFor(A, 'a', int)
        a = A()
        self.assertRaises(ValueError, setattr, a, 'a', 'ola')
        a.a = 12


if __name__ == '__main__':
    unittest.main()