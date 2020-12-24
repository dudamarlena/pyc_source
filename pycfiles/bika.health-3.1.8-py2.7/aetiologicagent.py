# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/aetiologicagent.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.lims.browser.widgets import RecordsWidget
from bika.lims.content.bikaschema import BikaSchema
from bika.health.config import PROJECTNAME
from Products.Archetypes.public import *
from Products.ATExtensions.ateapi import RecordsField
from zope.interface import implements
schema = BikaSchema.copy() + Schema((
 RecordsField('AetiologicAgentSubtypes', type='aetiologicagentsubtypes', subfields=('Subtype',
                                                                                   'SubtypeRemarks'), subfield_labels={'Subtype': _('Subtype'), 'SubtypeRemarks': _('Remarks')}, subfield_sizes={'Subtype': 10, 'SubtypeRemarks': 25}, widget=RecordsWidget(label='Subtypes', description=_('A list of aetiologic agent subtypes.'), visible=True)),))
schema['description'].widget.visible = True
schema['description'].schemata = 'default'

class AetiologicAgent(BaseContent):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


registerType(AetiologicAgent, PROJECTNAME)