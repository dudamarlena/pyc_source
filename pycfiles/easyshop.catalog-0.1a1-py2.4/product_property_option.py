# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/content/product_property_option.py
# Compiled at: 2008-09-03 11:14:29
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IPropertyOption
schema = Schema((ImageField(name='image', sizes={'listing': (16, 16)}, widget=ImageWidget(label='Image', label_msgid='schema_image_label', i18n_domain='EasyShop'), storage=AttributeStorage()), FloatField(name='price', default=0.0, widget=DecimalWidget(size='10', label='Price', label_msgid='schema_price_label', i18n_domain='EasyShop'))))

class ProductPropertyOption(BaseContent):
    """
    """
    __module__ = __name__
    implements(IPropertyOption)
    schema = BaseContent.schema.copy() + schema
    _at_rename_after_creation = True

    def base_view(self):
        """Overwritten to redirect to manage-properties-view of parent product 
        or group.
        """
        parent = self.aq_inner.aq_parent
        grant_parent = parent.aq_inner.aq_parent
        url = grant_parent.absolute_url() + '/' + 'manage-properties-view'
        self.REQUEST.RESPONSE.redirect(url)


registerType(ProductPropertyOption, PROJECTNAME)