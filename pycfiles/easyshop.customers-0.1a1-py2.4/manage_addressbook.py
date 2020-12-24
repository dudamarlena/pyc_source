# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/browser/manage_addressbook.py
# Compiled at: 2008-09-03 11:14:43
from Products.Five.browser import BrowserView
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IAddressManagement

class ManageAddressBookView(BrowserView):
    """
    """
    __module__ = __name__

    def deleteAddress(self):
        """
        """
        toDeleteAddressId = self.context.request.get('id')
        am = IAddressManagement(self.context)
        am.deleteAddress(toDeleteAddressId)
        putils = getToolByName(self.context, 'plone_utils')
        putils.addPortalMessage(_('The address has been deleted.'))
        url = '%s/manage-addressbook' % self.context.absolute_url()
        self.context.request.response.redirect(url)