# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/group.py
# Compiled at: 2008-09-03 11:14:39
import transaction
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IGroupCriteria
from easyshop.core.interfaces import IShopManagement
schema = Schema((StringField(name='title', widget=StringWidget(visible={'edit': 'invisible', 'view': 'invisible'}, label='Title', label_msgid='schema_title_label', i18n_domain='EasyShop'), required=0), LinesField(name='groups', widget=MultiSelectionWidget(label='Groups', label_msgid='schema_groups_label', i18n_domain='EasyShop'), multiValued=1, vocabulary='_getGroupsAsDL')))

class GroupCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IGroupCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return 'Groups'

    def getValue(self):
        """
        """
        return (', ').join(self.getGroups())

    def _getGroupsAsDL(self):
        """Returns all Categories as DisplayList
        """
        shop = IShopManagement(self).getShop()
        dl = DisplayList()
        catalog = getToolByName(self, 'portal_catalog')
        brains = catalog.searchResults(path=('/').join(shop.getPhysicalPath()), portal_type='ProductGroup')
        for brain in brains:
            dl.add(brain.id, brain.Title)

        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id"""
        transaction.commit()
        new_id = 'GroupCriteria'
        self.setId(new_id)


registerType(GroupCriteria, PROJECTNAME)