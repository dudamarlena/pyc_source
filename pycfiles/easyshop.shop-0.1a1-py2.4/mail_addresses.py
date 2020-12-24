# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/mail_addresses.py
# Compiled at: 2008-09-03 11:15:25
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from Products.CMFCore.interfaces import ISiteRoot
from easyshop.core.interfaces import IMailAddresses
from easyshop.core.interfaces import IShop

class ShopMailAddresses(object):
    """An adapter which provides IMailAddresses for shop content objects.
    """
    __module__ = __name__
    implements(IMailAddresses)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getSender(self):
        """Returns sender from shop content object. If it is blank returns Plone
        default sender. If it is also blank returns None.
        """
        name = self.context.getMailFromName()
        if name == '':
            name = getUtility(ISiteRoot).email_from_name
        address = self.context.getMailFromAddress()
        if address == '':
            address = getUtility(ISiteRoot).email_from_address
        if address == '':
            return
        if name != '':
            return '%s <%s>' % (name, address)
        else:
            return address
        return

    def getReceivers(self):
        """Returns receivers from shop content object. If they are blank 
        returns Plone default receiver. If it is also blank returns None.
        """
        receivers = self.context.getMailTo()
        if len(receivers) == 0:
            sender = self.getSender()
            if sender is None:
                return ()
            else:
                return (
                 sender,)
        else:
            return receivers
        return