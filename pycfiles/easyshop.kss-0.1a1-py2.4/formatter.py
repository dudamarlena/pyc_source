# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/kss/formatter.py
# Compiled at: 2008-09-03 11:14:57
from zope.component.exceptions import ComponentLookupError
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from easyshop.core.interfaces import IFormats

class FormatterKSSView(PloneKSSView):
    """
    """
    __module__ = __name__

    @kssaction
    def saveFormatter(self, portlethash):
        """
        """
        fi = IFormats(self.context)
        fi.setFormats(self.request.form)
        kss_core = self.getCommandSet('core')
        kss_zope = self.getCommandSet('zope')
        kss_plone = self.getCommandSet('plone')
        layout = self.request.form.get('layout')
        if layout == 'categories-view':
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector('categories-list'), manager='easyshop.categories-manager', name='easyshop.categories-viewlet')
        elif layout == 'products-view':
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector('products-list'), manager='easyshop.products-manager', name='easyshop.products-viewlet')
        elif layout == 'product-selector-view':
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector('products-list'), manager='easyshop.product-selector-manager', name='easyshop.product-selector-viewlet')
        elif layout == 'overview':
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector('products-list'), manager='easyshop.products-manager', name='easyshop.products-viewlet')
        kss_plone.refreshPortlet(portlethash)