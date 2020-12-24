# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/adapters/widgetvisibility.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.WorkflowCore import WorkflowException
from bika.lims.utils import getHiddenAttributesForClass
from types import DictType
from Products.CMFCore.utils import getToolByName
from bika.lims.interfaces import IATWidgetVisibility
from zope.interface import implements
from bika.health.permissions import ViewPatients
_marker = []

class PatientFieldsWidgetVisibility(object):
    """This will force readonly fields to be uneditable, and viewable only by
     those with ViewPatients permission.
    """
    implements(IATWidgetVisibility)

    def __init__(self, context):
        self.context = context

    def __call__(self, context, mode, field, default):
        state = default if default else 'invisible'
        header_table_fields = [
         'Patient',
         'PatientID',
         'ClientPatientID']
        readonly_fields = ['Batch',
         'Patient',
         'PatientID',
         'ClientPatientID']
        mtool = getToolByName(self.context, 'portal_membership')
        has_perm = mtool.checkPermission(ViewPatients, self.context)
        fieldName = field.getName()
        if fieldName not in header_table_fields and fieldName not in readonly_fields:
            return state
        if has_perm:
            if mode == 'header_table' and fieldName in header_table_fields:
                state = 'visible'
            if mode == 'view' and fieldName in readonly_fields:
                state = 'visible'
        if mode == 'edit' and fieldName in readonly_fields:
            state = 'invisible'
        return state