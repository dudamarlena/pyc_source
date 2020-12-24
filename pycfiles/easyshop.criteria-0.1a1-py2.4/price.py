# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/price.py
# Compiled at: 2008-09-03 11:14:39
from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IPriceCriteria
schema = Schema((FloatField(name='price', default=0.0, widget=DecimalWidget(label='Price', label_msgid='schema_price_label', description='Valid if the cart price is greater than or equal price you enter here.', description_msgid='schema_price_description', i18n_domain='EasyShop')), StringField(name='priceType', vocabulary='_getPriceTypesAsDL', default='net', widget=SelectionWidget(label='Price Type', label_msgid='schema_price_label', description='Please select the type of the entered price above.', description_msgid='schema_price_type_description', i18n_domain='EasyShop'))))

class PriceCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IPriceCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return 'Price'

    def getValue(self):
        """
        """
        return self.getPrice()

    def _getPriceTypesAsDL(self):
        """Returns vocabulary for field "price_type" as DisplayList.
        """
        dl = DisplayList()
        dl.add('gross', 'Gross')
        dl.add('net', 'Net')
        return dl


registerType(PriceCriteria, PROJECTNAME)