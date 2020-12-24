# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/testX509.py
# Compiled at: 2012-03-06 02:26:51
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from unittest import TestCase, TestSuite, makeSuite
from Testing import ZopeTestCase
from Products.BastionCrypto import BastionX509Generator

class TestX509(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        BastionX509Generator.manage_addBastionX509Generator(self.app.test_folder_1_, 'x509')
        self.x509 = self.app.test_folder_1_.x509

    def testCreated(self):
        self.failUnless(hasattr(self.app.test_folder_1_, 'x509'))

    def XtestGenerate(self):
        self.pks.generate()
        self.assertEqual(key.getId(), '846B1B0423636051')


if __name__ == '__main__':
    framework()
else:

    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestX509))
        return suite