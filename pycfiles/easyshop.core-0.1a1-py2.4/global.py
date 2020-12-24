# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/browser/global.py
# Compiled at: 2008-06-20 09:35:26
from zope.interface import Interface
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class EasyShopView(BrowserView):
    """
    """
    __module__ = __name__

    def disableBorder(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.checkPermission('Manage portal', self.context):
            self.request.set('disable_border', 1)