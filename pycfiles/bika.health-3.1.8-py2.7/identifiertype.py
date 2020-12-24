# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/identifiertype.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import registerType
from bika.lims.content.bikaschema import BikaSchema
from bika.health.config import PROJECTNAME
schema = BikaSchema.copy()
schema['description'].widget.visible = True
schema['description'].schemata = 'default'

class IdentifierType(BaseContent):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


registerType(IdentifierType, PROJECTNAME)