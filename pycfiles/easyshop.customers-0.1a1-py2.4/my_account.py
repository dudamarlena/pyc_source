# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/portlets/my_account.py
# Compiled at: 2008-09-03 11:14:43
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement
_ = MessageFactory('EasyShop')

class IMyAccountPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IMyAccountPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('My Account')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('my_account.pt')

    @property
    def available(self):
        """
        """
        return True

    @memoize
    def getMyAccountUrl(self):
        """
        """
        customer = self.getCustomer()
        return '%s/my-account' % customer.absolute_url()

    @memoize
    def getPortalUrl(self):
        """
        """
        utool = getToolByName(self.context, 'portal_url')
        return utool.getPortalObject().absolute_url()

    @memoize
    def getUserName(self):
        """
        """
        customer = self.getCustomer()
        return customer.Title()

    @memoize
    def isAnonymous(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.isAnonymousUser()

    @memoize
    def getCustomer(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return ICustomerManagement(shop).getAuthenticatedCustomer()


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()