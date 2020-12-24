# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/utils/workgroup_actions.py
# Compiled at: 2008-06-25 09:09:13
from zope.interface import implements
from zope.interface import noLongerProvides
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from redomino.workgroup.interfaces import IWorkgroup
from redomino.workgroup.utils.interfaces import IWorkgroupActions

class WorkgroupActions(object):
    """ WorkgroupActions utility """
    __module__ = __name__
    implements(IWorkgroupActions)
    _WORKGROUP_MEMBERDATA = 'workgroup_memberdata'

    def disable(self, context):
        """ Disable workgroup action """
        noLongerProvides(context, IWorkgroup)
        if context.hasObject(self._WORKGROUP_MEMBERDATA):
            wg_memberdata = getattr(context, self._WORKGROUP_MEMBERDATA)
            wg_memberdata.unindexObject()

    def enable(self, context):
        """ Enable workgroup action"""
        portal_types = getToolByName(context, 'portal_types')
        try:
            if not context.hasObject(self._WORKGROUP_MEMBERDATA):
                portal_types.constructContent('MemberArea', context, self._WORKGROUP_MEMBERDATA)
            wg_memberdata = getattr(context, self._WORKGROUP_MEMBERDATA)
            wg_memberdata.unindexObject()
        except:
            raise
        else:
            alsoProvides(context, IWorkgroup)