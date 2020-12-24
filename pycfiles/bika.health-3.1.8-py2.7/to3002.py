# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to3002.py
# Compiled at: 2014-12-12 07:13:54
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    client = portal.portal_types.getTypeInfo('Client')
    client.addAction(id='patients', name='Patients', action='string:${object_url}/patients', permission='BIKA: Edit Patient', category='object', visible=True, icon_expr='string:${portal_url}/images/patient.png', link_target='', description='', condition='')
    return True