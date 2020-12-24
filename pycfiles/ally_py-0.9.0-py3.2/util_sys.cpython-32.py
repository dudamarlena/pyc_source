# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/support/util_sys.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 1, 2012

@package: ally base
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Testing for the  classes utility.
"""
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