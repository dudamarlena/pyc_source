# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/portlets/admin.py
# Compiled at: 2008-09-03 11:15:26
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
_ = MessageFactory('EasyShop')
from easyshop.core.interfaces import IShopManagement

class IAdminPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IAdminPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('EasyShop Manager')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('admin.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('Manage portal', self.context):
            return True
        else:
            return False

    def getShopURL(self):
        """
        """
        return IShopManagement(self.context).getShop().absolute_url()


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()