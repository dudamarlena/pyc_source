# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/information/portlets/information.py
# Compiled at: 2008-09-03 11:14:54
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.config import _
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IInformationManagement

class IInformationPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IInformationPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('EasyShop: Information')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('information.pt')

    def update(self):
        """
        """
        self.information = self._information()

    @memoize
    def _information(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        im = IInformationManagement(shop)
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == False:
            information = im.getInformationPagesFor(self.context)
        else:
            product_variant = pvm.getSelectedVariant()
            information = im.getInformationPagesFor(product_variant)
            if information is None:
                information = im.getInformationPagesFor(self.context)
        return information

    @property
    def available(self):
        """
        """
        return len(self._information()) > 0


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()