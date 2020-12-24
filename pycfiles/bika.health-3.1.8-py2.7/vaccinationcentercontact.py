# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/vaccinationcentercontact.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import manage_users
from Products.Archetypes.public import *
from bika.lims.content.person import Person
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from bika.health.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from zope.interface import implements
schema = Person.schema.copy()
schema['JobTitle'].schemata = 'default'
schema['Department'].schemata = 'default'
schema['id'].schemata = 'default'
schema['id'].widget.visible = False
schema['title'].schemata = 'default'
schema['title'].required = 0
schema['title'].widget.visible = False

class VaccinationCenterContact(Person):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


registerType(VaccinationCenterContact, PROJECTNAME)