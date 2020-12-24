# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/tests/testBank.py
# Compiled at: 2015-07-18 19:38:10
from Testing import ZopeTestCase
from Products.PloneTestCase.PloneTestCase import PloneTestCase
ZopeTestCase.installProduct('BastionBanking')
ZopeTestCase.installProduct('ZCatalog')
ZopeTestCase.installProduct('TextIndexNG3')
from ..config import BANKTOOL

class TestBastionBanking(PloneTestCase):

    def testCreation(self):
        self.app.manage_addProduct['BastionBanking'].manage_addBastionBankService('ManualPayment')
        self.failUnless(getattr(self.app, BANKTOOL, None))
        return


from unittest import TestSuite, makeSuite

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestBastionBanking))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')