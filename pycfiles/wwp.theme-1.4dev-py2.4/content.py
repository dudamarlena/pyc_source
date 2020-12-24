# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/browser/content.py
# Compiled at: 2009-09-25 07:29:06
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from zope.component import getMultiAdapter, queryMultiAdapter
from plone.memoize.instance import memoize
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import log
import logging

class DocumentActionsViewlet(ViewletBase):
    __module__ = __name__

    def update(self):
        super(DocumentActionsViewlet, self).update()
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
        self.actions = self.context_state.actions().get('document_actions', None)
        return

    index = ViewPageTemplateFile('templates/document_actions.pt')