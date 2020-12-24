# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/core/spec/resources.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 21, 2012\n\n@package: ally core\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nResources testing.\n'
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