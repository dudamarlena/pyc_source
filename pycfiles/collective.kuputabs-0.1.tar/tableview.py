# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/browser/views/tableview.py
# Compiled at: 2008-11-11 03:32:56
from plone.app.content.browser import tableview
from Products.Archetypes.interfaces.base import IBaseObject
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from zope.app.pagetemplate import ViewPageTemplateFile
from Acquisition import aq_inner

class Table(tableview.Table):
    __module__ = __name__

    def __init__(self, request, base_url, view_url, items, show_sort_column=False, buttons=[], pagesize=20, context=None):
        tableview.Table.__init__(self, request, base_url, view_url, items, show_sort_column, buttons, pagesize)
        self.context = context

    def render(self, *args, **kwargs):
        pt = ViewPageTemplateFile('table.pt')
        return pt(self, *args, **kwargs)

    def editable(self, obj=None, item={}, return_object_if_true=False):
        context = aq_inner(self.context)
        kssinline = getToolByName(context, 'portal_kssinline', None)
        if kssinline is None:
            return False
        if obj is None:
            portal = getToolByName(context, 'portal_url').getPortalObject()
            obj = portal.restrictedTraverse(item['path']())
        pms = getToolByName(self.context, 'portal_membership')
        member = pms.getAuthenticatedMember()
        result = IBaseObject.isImplementedBy(obj) and getattr(obj, 'portal_type', '') in kssinline.getEditableTypes() and member.has_permission(ModifyPortalContent, obj)
        if not result:
            return False
        if return_object_if_true:
            return obj
        return