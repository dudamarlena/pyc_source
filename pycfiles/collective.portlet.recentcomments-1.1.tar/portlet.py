# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/portlet.py
# Compiled at: 2010-05-19 10:20:52
import time
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from zope.component import getUtility
from collective.portlet.recentactivity import RecentActivityPortletMessageFactory as _
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility
from collective.portlet.recentactivity.interfaces import IRecentActivityPortlet
from utils import compute_time

class IRecentActivityPortlet(IPortletDataProvider):
    __module__ = __name__
    count = schema.Int(title=_('Number of items to display'), description=_('How many items to list.'), required=True, default=5)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IRecentActivityPortlet)

    def __init__(self, count=5):
        self.count = count

    @property
    def title(self):
        return _('Recent Activity Portlet')


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(IRecentActivityPortlet)
    label = _('Add Recent Activity Portlet')
    description = _('This portlet displays recently modified content.')

    def create(self, data):
        return Assignment(count=data.get('count', 5))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(IRecentActivityPortlet)
    label = _('Edit Recent Portlet')
    description = _('This portlet displays recently modified content.')


class Renderer(base.Renderer):
    __module__ = __name__
    _template = ViewPageTemplateFile('portlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.portal_url = portal_state.portal_url()
        self.typesToShow = portal_state.friendly_types()
        plone_tools = getMultiAdapter((context, self.request), name='plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return not self.anonymous

    def has_recent_activities(self):
        return self._data()

    @memoize
    def recent_activities(self):
        context = aq_inner(self.context)
        for brain in self._data():
            activity = brain[1]
            yield dict(time=compute_time(int(time.time()) - brain[0]), action=activity['action'], user=activity['user'], user_url='%s/author/%s' % (context.portal_url(), activity['user']), object=activity['object'], object_url=activity['object_url'], parent=activity['parent'], parent_url=activity['parent_url'])

    def recently_modified_link(self):
        return '%s/@@recent-activity' % self.portal_url

    @memoize
    def _data(self):
        limit = self.data.count
        activities = getUtility(IRecentActivityUtility)
        return activities.getRecentActivity(limit)