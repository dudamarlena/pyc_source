# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/portlet/z3cformhelper.py
# Compiled at: 2015-10-13 13:57:55
import time
from z3c.form import button
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import implements
from Acquisition import aq_parent, aq_inner
try:
    from plone.app.portlets import PloneMessageFactory as _
    PLONE4 = True
except ImportError:

    def _(x, default=''):
        if default != '':
            return default
        return x


    PLONE4 = False

from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker

def getSiteRootRelativePath(context, request):
    """ Get site root relative path to an item

    @param context: Content item which path is resolved

    @param request: HTTP request object

    @return: Path to the context object, relative to site root, prefixed with a slash.
    """
    portal_state = getMultiAdapter((context, request), name='plone_portal_state')
    site = portal_state.portal()
    site_path = site.getPhysicalPath()
    if not hasattr(context, 'getPhysicalPath'):
        context = context.context
    context_path = context.getPhysicalPath()
    relative_path = context_path[len(site_path):]
    return '/' + ('/').join(relative_path)


class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label = _('Configure portlet')

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        addview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(addview))
        url = str(getMultiAdapter((context, self.request), name='absolute_url'))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_('label_save', default='Save'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            obj = self.createAndAdd(data)
            if obj is not None:
                self._finishedAdd = True
                column = self.context.aq_parent
                path = getSiteRootRelativePath(column, self.request)
                obj.contextPath = path + '/' + obj.getId()
            return

    @button.buttonAndHandler(_('label_cancel', default='Cancel'), name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''


class EditForm(form.EditForm):
    """An edit form for portlets.
    """
    implements(IPortletEditForm)
    label = _('Modify portlet')

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request), name='absolute_url'))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_('label_save', default='Save'), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = 'Changes saved'
        else:
            self.status = 'No changes'
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_('label_cancel', default='Cancel'), name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''