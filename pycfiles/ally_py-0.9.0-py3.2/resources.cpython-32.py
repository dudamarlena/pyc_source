# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/core/spec/resources.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 21, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Resources testing.
"""
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.api.type import Boolean, typeFor, Integer
from ally.core.spec.resources import Converter
import unittest

class TestConversion(unittest.TestCase):

    def testConversion(self):
        converter = Converter()
        self.assertEqual(converter.asValue('10', typeFor(Integer)), 10)
        self.assertEqual(converter.asValue('false', typeFor(Boolean)), False)


if __name__ == '__main__':
    unittest.main()