# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_mail_addresses.py
# Compiled at: 2008-06-20 09:37:19
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.mail import IMailSchema
from base import EasyShopTestCase
from easyshop.core.interfaces import IMailAddresses

class TestShopMailAddresses(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestShopMailAddresses, self).afterSetUp()
        self.addresses = IMailAddresses(self.shop)

    def testGetAddresses1(self):
        """No information entered.
        """
        sender = self.addresses.getSender()
        self.assertEqual(sender, None)
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ())
        return

    def testGetAddresses2(self):
        """Information entered in portal. Note: Portal has just one email 
        address which is used for sender and receiver.
        """
        utool = getToolByName(self.shop, 'portal_url')
        portal = utool.getPortalObject()
        mail = IMailSchema(portal)
        mail.set_email_from_address('john@doe.com')
        sender = self.addresses.getSender()
        self.assertEqual(sender, 'Site Administrator <john@doe.com>')
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('Site Administrator <john@doe.com>', ))
        mail.set_email_from_name('John Doe')
        sender = self.addresses.getSender()
        self.assertEqual(sender, 'John Doe <john@doe.com>')
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('John Doe <john@doe.com>', ))

    def testGetAddresses3(self):
        """Information entered in shop.
        """
        self.shop.setMailFromAddress('john@doe.com')
        sender = self.addresses.getSender()
        self.assertEqual(sender, 'Site Administrator <john@doe.com>')
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('Site Administrator <john@doe.com>', ))
        self.shop.setMailFromName('John Doe')
        sender = self.addresses.getSender()
        self.assertEqual(sender, 'John Doe <john@doe.com>')
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('John Doe <john@doe.com>', ))
        self.shop.setMailTo(['Jane Doe <jane@doe.com>'])
        sender = self.addresses.getSender()
        self.assertEqual(sender, 'John Doe <john@doe.com>')
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('Jane Doe <jane@doe.com>', ))
        self.shop.setMailTo(['Jane Doe <jane@doe.com>', 'baby@joe.com'])
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ('Jane Doe <jane@doe.com>', 'baby@joe.com'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopMailAddresses))
    return suite