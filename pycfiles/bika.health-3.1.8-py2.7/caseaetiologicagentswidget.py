# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/widgets/caseaetiologicagentswidget.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from bika.lims.browser.widgets import RecordsWidget
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.lims.browser import BrowserView
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.idserver import renameAfterCreation
from bika.health.permissions import *
from operator import itemgetter
import json, plone

class CaseAetiologicAgentsWidget(RecordsWidget):
    _properties = RecordsWidget._properties.copy()
    _properties.update({'helper_js': ('bika_health_widgets/caseaetiologicagentswidget.js', )})


registerWidget(CaseAetiologicAgentsWidget, title='Aetiologic agents', description="Laboratory confirmed aetiologic agent and subtype, as the disease's cause")