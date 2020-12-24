# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/browser/product_view.py
# Compiled at: 2008-09-03 11:14:28
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IProductVariantsManagement

class ProductView(BrowserView):
    """
    """
    __module__ = __name__

    def __call__(self):
        """
        """
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == True and self.request.get('variant_selected', None) is not None:
            selected_variant = pvm.getSelectedVariant()
            if selected_variant is None:
                putils = getToolByName(self.context, 'plone_utils')
                putils.addPortalMessage(MESSAGES['VARIANT_DONT_EXIST'])
        return super(ProductView, self).__call__()