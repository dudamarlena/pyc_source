# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.network/plonesocial/network/browser/profile.py
# Compiled at: 2013-09-11 10:31:05
from zope.interface import implements, Interface
from zope.component import adapts
from zope.component import getMultiAdapter, ComponentLookupError
from zope.component import queryUtility
from zope.publisher.interfaces import IPublishTraverse
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.globals.interfaces import IViewView
from plonesocial.network.interfaces import INetworkGraph
from .interfaces import IPlonesocialNetworkLayer
from .interfaces import IProfileProvider
import logging
logger = logging.getLogger('plonesocial.network.profile')

class AbstractProfile(object):

    def render(self):
        return self.index()

    __call__ = render

    @property
    def viewer_id(self):
        """The guy looking at the profile"""
        return self.mtool.getAuthenticatedMember().getId()

    @property
    def data(self):
        return self.mtool.getMemberInfo(self.userid)

    @property
    def portrait(self):
        """Mugshot."""
        return self.mtool.getPersonalPortrait(self.userid)

    @property
    def is_anonymous(self):
        return self.mtool.isAnonymousUser()

    @property
    def is_mine(self):
        """Is this my own profile, or somebody else's?"""
        return self.userid == self.viewer_id

    @property
    def is_following(self):
        return self.userid in self.graph.get_following(self.viewer_id)

    @property
    def show_subunsub(self):
        return not (self.is_anonymous or self.is_mine)

    @property
    def mtool(self):
        return getToolByName(getSite(), 'portal_membership')

    @property
    def graph(self):
        return queryUtility(INetworkGraph)

    def portal_url(self):
        portal_state = getMultiAdapter((
         self.context, self.request), name='plone_portal_state')
        return portal_state.portal_url()

    def profile_url(self):
        return self.portal_url() + '/@@profile/' + self.userid

    def following_url(self):
        return self.portal_url() + '/@@following/' + self.userid

    def followers_url(self):
        return self.portal_url() + '/@@followers/' + self.userid

    def following_count(self):
        return len(self.graph.get_following(self.userid))

    def followers_count(self):
        return len(self.graph.get_followers(self.userid))


class AbstractProfileProvider(AbstractProfile):

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = self.__parent__ = view
        self.userid = None
        return

    def __call__(self):
        userid = self.request.form.get('userid', None)
        if userid is None:
            return self.render()
        else:
            if userid is not None and userid == self.userid:
                followaction = self.request.form.get('subunsub_follow', None)
                unfollowaction = self.request.form.get('subunsub_unfollow', None)
                if followaction:
                    self.graph.set_follow(self.viewer_id, userid)
                    logger.info('%s follows %s', self.viewer_id, userid)
                else:
                    if unfollowaction:
                        self.graph.set_unfollow(self.viewer_id, userid)
                        logger.info('%s unfollowed %s', self.viewer_id, userid)
                    if followaction or unfollowaction:
                        self.request.response.redirect(self.request.URL)
                        return ''
            return self.render()


class MaxiProfileProvider(AbstractProfileProvider):
    implements(IProfileProvider)
    adapts(Interface, IPlonesocialNetworkLayer, Interface)
    index = ViewPageTemplateFile('templates/maxiprofile_provider.pt')


class MiniProfileProvider(AbstractProfileProvider):
    implements(IProfileProvider)
    adapts(Interface, IPlonesocialNetworkLayer, Interface)
    index = ViewPageTemplateFile('templates/miniprofile_provider.pt')


class ProfileView(BrowserView, AbstractProfile):
    implements(IPublishTraverse, IViewView)
    index = ViewPageTemplateFile('templates/profile.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._userid = None
        return

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        self._userid = name
        return self

    @property
    def userid(self):
        """The guy in the profile"""
        if self._userid:
            return self._userid
        else:
            if self.is_anonymous:
                return
            else:
                return self.viewer_id

            return

    def stream_provider(self):
        try:
            provider = getMultiAdapter((
             self.context, self.request, self), name='plonesocial.activitystream.stream_provider')
            provider.users = self.userid
            return provider()
        except ComponentLookupError:
            return ''

    def maxiprofile_provider(self, userid):
        provider = getMultiAdapter((
         self.context, self.request, self), name='plonesocial.network.maxiprofile_provider')
        provider.userid = userid
        return provider()