# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/browser/stream_provider.py
# Compiled at: 2014-02-04 02:59:10
import itertools
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getMultiAdapter
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from Acquisition import aq_inner
from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from zExceptions import NotFound
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plonesocial.activitystream.interfaces import IActivity
from .interfaces import IPlonesocialActivitystreamLayer
from .interfaces import IStreamProvider
from .interfaces import IActivityProvider
from plonesocial.activitystream.integration import PLONESOCIAL
import logging
logger = logging.getLogger(__name__)

def date_key(item):
    if hasattr(item, 'effective'):
        return max(item.effective, item.created)
    return item.date


class StreamProvider(object):
    """Render activitystreams

    This is the core rendering logic that powers
    @@stream and @@activitystream_portal, and also
    plonesocial.networking @@profile
    """
    implements(IStreamProvider)
    adapts(Interface, IPlonesocialActivitystreamLayer, Interface)
    index = ViewPageTemplateFile('templates/stream_provider.pt')

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = self.__parent__ = view
        self.portlet_data = None
        self.tag = None
        self.users = None
        self.microblog_context = PLONESOCIAL.context(context)
        return

    def update(self):
        pass

    def render(self):
        return self.index()

    __call__ = render

    def activities(self):
        brains = self._activities_brains()
        statuses = self._activities_statuses()
        items = itertools.chain(brains, statuses)
        items = sorted(items, key=date_key, reverse=True)
        i = 0
        for item in items:
            if i >= self.count:
                break
            try:
                activity = IActivity(item)
            except Unauthorized:
                continue
            except NotFound:
                logger.exception('NotFound: %s' % item.getURL())
                continue

            if self._activity_visible(activity):
                yield activity
                i += 1

    def _activity_visible(self, activity):
        if activity.is_status and self.show_microblog:
            return True
        if activity.is_content and self.show_content:
            return True
        if activity.is_discussion and self.show_discussion:
            return True
        return False

    def _activities_brains(self):
        if not self.show_content and not self.show_discussion:
            return []
        catalog = getToolByName(self.context, 'portal_catalog')
        contentfilter = dict(sort_on='Date', sort_order='reverse', sort_limit=self.count * 10)
        if self.tag:
            contentfilter['Subject'] = self.tag
        if self.users:
            contentfilter['Creator'] = self.users
        elif self.microblog_context:
            contentfilter['path'] = ('/').join(self.microblog_context.getPhysicalPath())
        return catalog.searchResults(**contentfilter)

    def _activities_statuses(self):
        if not self.show_microblog:
            return []
        container = PLONESOCIAL.microblog
        if not container:
            return []
        try:
            if self.users:
                return container.user_values(self.users, limit=self.count, tag=self.tag)
            else:
                if self.microblog_context:
                    return container.context_values(self.microblog_context, limit=self.count, tag=self.tag)
                return container.values(limit=self.count, tag=self.tag)

        except Unauthorized:
            return []

    def activity_providers(self):
        for activity in self.activities():
            if not self.can_view(activity):
                continue
            yield getMultiAdapter((
             activity, self.request, self.view), IActivityProvider, name='plonesocial.activitystream.activity_provider')

    def can_view(self, activity):
        """Returns true if current user has the 'View' permission.
        """
        sm = getSecurityManager()
        if activity.is_status:
            permission = 'Plone Social: View Microblog Status Update'
            return sm.checkPermission(permission, self.context)
        if activity.is_discussion:
            return sm.checkPermission('View', aq_inner(activity.context)) and sm.checkPermission('View', aq_inner(activity.context).__parent__.__parent__)
        if activity.is_content:
            return sm.checkPermission('View', aq_inner(activity.context))

    def is_anonymous(self):
        portal_membership = getToolByName(getSite(), 'portal_membership', None)
        return portal_membership.isAnonymousUser()

    @property
    def count(self):
        if self.portlet_data:
            return self.portlet_data.count
        return 15

    @property
    def show_microblog(self):
        if self.portlet_data:
            return self.portlet_data.show_microblog
        return True

    @property
    def show_content(self):
        if self.portlet_data:
            return self.portlet_data.show_content
        return True

    @property
    def show_discussion(self):
        if self.portlet_data:
            return self.portlet_data.show_discussion
        return True