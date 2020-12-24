# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/browser/workgroup_form.py
# Compiled at: 2008-06-25 09:09:13
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
from zope.formlib import form
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _
from redomino.workgroup.interfaces import IWorkgroup
from redomino.workgroup.utils.interfaces import IWorkgroupActions

class WorkgroupEnableForm(PageForm):
    __module__ = __name__
    form_fields = []
    label = 'Enable workgroup management'

    @form.action('Enable workgroup')
    def enable_workgroup(self, action, data):
        context = self.context
        wg_util = queryUtility(IWorkgroupActions)
        wg_util.enable(context)
        status_message = 'Enabled workgroup'
        url = getMultiAdapter((context, self.request), name='absolute_url')()
        IStatusMessage(self.request).addStatusMessage(_(status_message), type='info')
        self.request.response.redirect(url)
        return ''


class WorkgroupDisableForm(PageForm):
    __module__ = __name__
    form_fields = []
    label = 'Disable workgroup management'

    @form.action('Disable workgroup')
    def disable_workgroup(self, action, data):
        context = self.context
        if len(context.restrictedTraverse('@@pas_search').searchUsers()) > 0:
            status_message = 'workgroup not disabled: you must delete all workgroup users first!'
        else:
            wg_util = queryUtility(IWorkgroupActions)
            wg_util.disable(context)
            status_message = 'Disabled workgroup'
        url = getMultiAdapter((context, self.request), name='absolute_url')()
        IStatusMessage(self.request).addStatusMessage(_(status_message), type='info')
        self.request.response.redirect(url)
        return ''