# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/testZopeRepository.py
# Compiled at: 2012-03-06 02:26:51
"""
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.BastionCrypto.tests.CryptoTestCase import CryptoTestCase

class TestZopeRepository(CryptoTestCase):

    def testCreated(self):
        self.failUnless(self.pks)


if __name__ == '__main__':
    framework()
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestZopeRepository))
        return suite