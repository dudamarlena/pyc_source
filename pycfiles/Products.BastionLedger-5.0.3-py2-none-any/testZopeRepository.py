# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/testZopeRepository.py
# Compiled at: 2012-03-06 02:26:51
__doc__ = '\n'
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