# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/adapters/information_management.py
# Compiled at: 2008-09-03 11:14:54
from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IInformationManagement
from easyshop.core.interfaces import IValidity

class InformationManagement:
    """Adapter which provides InformationManagement for shop content objects.
    """
    __module__ = __name__
    implements(IInformationManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.information = context['information']

    def getInformationPage(self, id):
        """
        """
        try:
            return self.information[id]
        except KeyError:
            return

        return

    def getInformationPages(self):
        """
        """
        return self.information.objectValues()

    def getInformationPagesFor(self, product):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for information in self.information.objectValues():
            if IValidity(information).isValid(product) == False:
                continue
            if IValidity(information).isValid(product) == False:
                continue
            if mtool.checkPermission('View', information) != True:
                continue
            result.append({'title': information.Title(), 'id': information.getId()})

        return result