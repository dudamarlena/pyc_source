# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/browser/stream.py
# Compiled at: 2014-03-11 12:05:44
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.publisher.interfaces import IPublishTraverse
from plone.app.layout.globals.interfaces import IViewView
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plonesocial.activitystream.integration import PLONESOCIAL
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonesocial.activitystream')

class StreamView(BrowserView):
    """Standalone view, providing
    - microblog input
    - activitystream rendering (via stream provider)

    @@stream -> either: all activities, or
             -> my network activities (if plonesocial.network is installed)
    @@stream/explore -> all activities (if plonesocial.network is installed)
    @@stream/tag/foobar -> all activities tagged #foobar
    """
    implements(IPublishTraverse, IViewView)
    index = ViewPageTemplateFile('templates/stream.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.tag = None
        self.explore = True
        return

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def update(self):
        """Mute plone.app.z3cform.kss.validation AttributeError"""
        pass

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        if name == 'tag':
            stack = request.get('TraversalRequestNameStack')
            try:
                self.tag = stack.pop()
            except IndexError:
                self.tag = None

        elif name == 'network':
            self.explore = False
        return self

    @property
    def title(self):
        m_context = PLONESOCIAL.context(self.context)
        if m_context:
            return m_context.Title() + ' updates'
        else:
            if self.explore:
                return _('Explore')
            return _('My network')

    def status_provider(self):
        if not PLONESOCIAL.microblog:
            return ''
        provider = getMultiAdapter((
         self.context, self.request, self), name='plonesocial.microblog.status_provider')
        provider.update()
        return provider()

    def stream_provider(self):
        provider = getMultiAdapter((
         self.context, self.request, self), name='plonesocial.activitystream.stream_provider')
        provider.tag = self.tag
        if self.explore or self.tag:
            return provider()
        mtool = getToolByName(self.context, 'portal_membership')
        viewer_id = mtool.getAuthenticatedMember().getId()
        if mtool.isAnonymousUser() or not viewer_id:
            return provider()
        following = list(PLONESOCIAL.network.get_following(viewer_id))
        following.append(viewer_id)
        provider.users = following
        return provider()