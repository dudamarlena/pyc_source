# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/date.py
# Compiled at: 2008-09-03 11:14:39
import transaction
from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IDateCriteria
schema = Schema((StringField(name='title', widget=StringWidget(visible={'edit': 'invisible', 'view': 'invisible'}, label='Title', label_msgid='schema_title_label', i18n_domain='EasyShop'), required=0), DateTimeField(name='start', widget=CalendarWidget(label='Start', label_msgid='schema_start_label', i18n_domain='EasyShop')), DateTimeField(name='end', widget=CalendarWidget(label='End', label_msgid='schema_end_label', i18n_domain='EasyShop'))))

class DateCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IDateCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = 'DateCriteria'
        self.setId(new_id)

    def Title(self):
        """
        """
        return 'Date'

    def getValue(self):
        """
        """
        tool = getToolByName(self, 'translation_service')
        start = tool.ulocalized_time(self.getStart(), long_format=False)
        end = tool.ulocalized_time(self.getEnd(), long_format=False)
        return '%s - %s' % (start, end)


registerType(DateCriteria, PROJECTNAME)