# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/profile.py
# Compiled at: 2008-08-09 03:17:46
from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles

class HiddenProducts(object):
    """
    """
    __module__ = __name__
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return [
         'easyshop.carts', 'easyshop.catalog', 'easyshop.criteria', 'easyshop.customers', 'easyshop.discounts', 'easyshop.groups', 'easyshop.information', 'easyshop.kss', 'easyshop.login', 'easyshop.management', 'easyshop.order', 'easyshop.payment', 'easyshop.shipping', 'easyshop.shop', 'easyshop.stocks', 'easyshop.taxes']