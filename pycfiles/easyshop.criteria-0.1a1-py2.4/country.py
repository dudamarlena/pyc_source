# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/country.py
# Compiled at: 2008-09-03 11:14:39
from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import ICountryCriteria
from easyshop.core.interfaces import IShopManagement
schema = Schema((LinesField(name='countries', multiValued=1, vocabulary='_getCountriesAsDL', widget=MultiSelectionWidget(label='Countries', label_msgid='schema_value_label', i18n_domain='EasyShop')),))

class CountryCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(ICountryCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return 'Country'

    def getValue(self):
        """
        """
        return (', ').join(self.getCountries())

    def _getCountriesAsDL(self):
        """
        """
        dl = DisplayList()
        for country in IShopManagement(self).getShop().getCountries():
            dl.add(country, country)

        return dl


registerType(CountryCriteria, PROJECTNAME)