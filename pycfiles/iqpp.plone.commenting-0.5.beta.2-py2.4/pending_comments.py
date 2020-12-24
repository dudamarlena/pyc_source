# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/portlets/pending_comments.py
# Compiled at: 2007-10-06 06:19:54
from Acquisition import aq_inner
from zope.formlib import form
from zope.interface import implements
from zope import schema
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from iqpp.plone.commenting.interfaces import IGlobalCommenting

class IPendingCommentsPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__
    count = schema.Int(title=_('Number of objects to display'), description=_('How many objects to list.'), required=True, default=5)


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IPendingCommentsPortlet)

    def __init__(self, count=5):
        """
        """
        self.count = count

    @property
    def title(self):
        """
        """
        return _('Pending Comments')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('pending_comments.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Review comments', self.context)

    def Title(self):
        """
        """
        return _('Pending Comments')

    def pending_comments(self):
        """
        """
        return self._data()

    @memoize
    def _data(self):
        limit = self.data.count
        context = aq_inner(self.context)
        c = IGlobalCommenting(context)
        return c.getPendingComments()[:limit]


class AddForm(base.AddForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IPendingCommentsPortlet)
    label = _('Pending Comments')
    description = _('This portlet displays comments which have to be reviewed.')

    def create(self, data):
        """
        """
        return Assignment(count=data.get('count', 5))


class EditForm(base.EditForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IPendingCommentsPortlet)
    label = _('Pending Comments')
    description = _('This portlet displays comments which have to be reviewed.')