# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/viewlets/addresses.py
# Compiled at: 2008-09-03 11:14:43
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.interfaces import IAddressManagement

class AddressesViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('addresses.pt')

    def getAddresses(self):
        """
        """
        am = IAddressManagement(self.context)
        return am.getAddresses()