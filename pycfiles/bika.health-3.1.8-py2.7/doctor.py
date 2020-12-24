# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/content/doctor.py
# Compiled at: 2014-12-12 07:13:54
"""
"""
from Products.ATContentTypes.content import schemata
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.public import *
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from bika.health.config import *
from bika.health.interfaces import IDoctor
from bika.health.permissions import *
from bika.lims.content.contact import Contact
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from zope.interface import implements
schema = Contact.schema.copy() + Schema((
 StringField('DoctorID', required=1, searchable=True, widget=StringWidget(label=_('Doctor ID'))),))

class Doctor(Contact):
    implements(IDoctor)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema
    security.declarePublic('getSamples')

    def getSamples(self):
        bc = getToolByName(self, 'bika_catalog')
        return [ p.getObject() for p in bc(portal_type='Sample', getDoctorUID=self.UID()) ]

    security.declarePublic('getARs')

    def getARs(self, analysis_state):
        bc = getToolByName(self, 'bika_catalog')
        return [ p.getObject() for p in bc(portal_type='AnalysisRequest', getDoctorUID=self.UID()) ]


atapi.registerType(Doctor, PROJECTNAME)