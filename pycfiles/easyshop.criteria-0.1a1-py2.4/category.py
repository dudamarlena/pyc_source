# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/category.py
# Compiled at: 2008-09-03 11:14:39
import transaction
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import ICategoryCriteria
from easyshop.core.interfaces import IShopManagement
schema = Schema((StringField(name='title', widget=StringWidget(visible={'edit': 'invisible', 'view': 'invisible'}, label='Title', label_msgid='schema_title_label', i18n_domain='EasyShop'), required=0), LinesField(name='categories', widget=MultiSelectionWidget(label='Categories', label_msgid='schema_categories_label', i18n_domain='EasyShop'), multiValued=1, vocabulary='getCategoriesAsDL')))

class CategoryCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(ICategoryCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema

    def getCategoriesAsDL(self):
        """Returns all Categories as DisplayList
        """
        shop = IShopManagement(self).getShop()
        dl = DisplayList()
        catalog = getToolByName(self, 'portal_catalog')
        brains = catalog.searchResults(path=('/').join(shop.getPhysicalPath()), portal_type='Category')
        for brain in brains:
            dl.add(brain.getPath(), '%s (%s)' % (brain.Title, brain.getPath()))

        return dl

    def Title(self):
        """
        """
        return 'Category'

    def getValue(self):
        """
        """
        return (', ').join(self.getCategories())

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = 'CategoryCriteria'
        self.setId(new_id)


registerType(CategoryCriteria, PROJECTNAME)