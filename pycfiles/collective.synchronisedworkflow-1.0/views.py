# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/views.py
# Compiled at: 2009-07-12 11:14:04
from time import time
import re
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError
from twitter import TwitterError
try:
    from stripogram import html2text
    HAS_STRIPOGRAM = True
except ImportError:
    HAS_STRIPOGRAM = False

from DateTime import DateTime
from zope.interface import implements
from zope.component import getUtility, getAdapter, queryMultiAdapter, getAdapters
from zope.viewlet.interfaces import IViewletManager, IViewlet
from Acquisition import aq_inner
from Products.PythonScripts.standard import url_quote
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plone import memoize
from collective.sylvester.utils import cache_key_60
from interfaces import ISylvesterView, ICredentialsFormView, IPublishToTwitterFormView, ITwitterAPI, ITwitterCredentialsProvider
TEXT_URL_TO_ANCHOR = re.compile('(((f|ht){1}tp://)[-a-zA-Z0-9@:%_\\+.~#?&//=]+)', re.I | re.M)

def errorhandler(func):

    def new(self, *args, **kwargs):
        handle_error = kwargs.get('handle_error', True)
        if not handle_error:
            return func(self, *args)
        viewname = ''
        try:
            return func(self, *args)
        except TwitterError:
            viewname = '@@collective.sylvester.service-error'
        except URLError:
            viewname = '@@collective.sylvester.service-error'
        except HTTPError, e:
            if e.msg == 'Unauthorized':
                viewname = '@@collective.sylvester.auth-error'
            else:
                viewname = '@@collective.sylvester.unknown-error'
        except:
            viewname = '@@collective.sylvester.unknown-error'

        context = aq_inner(self.context)
        self.request.RESPONSE.redirect('%s/%s' % (context.absolute_url(), viewname))

    return new


class TwitterAPIAdapter(object):
    """
    Utilities are unique in-memory objects which means we
    cannot store authentication information on them. We 
    need this adapter to provide authentication information 
    to the TwitterAPI utility.
    """
    __module__ = __name__

    def __init__(self, context, username, password):
        self.context = context
        self.username = username
        self.password = password

    def wrapper(self, func_name, *args, **kwargs):
        func = getattr(self.context, func_name)
        kw = kwargs.copy()
        if kw.has_key('handle_error'):
            del kw['handle_error']
        return func(self.username, self.password, *args, **kw)

    def __getattr__(self, name):
        if hasattr(self.context, name):
            if name in self.context.__callable_functions__:
                return lambda *args, **kwargs: self.wrapper(name, *args, **kwargs)
            else:
                return getattr(self.context, name)
        return getattr(object, name)


class SylvesterView(BrowserView):
    __module__ = __name__
    implements(ISylvesterView)
    twitter = None

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self._setup_twitter_adapter()

    def name(self):
        return self.__name__

    def authenticate(self, redirect=False):
        res = self._setup_twitter_adapter()
        if not res and redirect:
            self.redirect_to_credentials_form()
        return res

    def redirect_to_credentials_form(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        self.request.response.redirect('%s/@@collective.sylvester.credentials-form?came_from=%s' % (portal.absolute_url(), url_quote(self.request.URL)))

    def _setup_twitter_adapter(self):
        (username, password) = ('', '')
        session = self.request.SESSION
        if session.has_key('collective.sylvester.twitter'):
            username = session['collective.sylvester.twitter']['username']
            password = session['collective.sylvester.twitter']['password']
        else:
            pms = getToolByName(self.context, 'portal_membership')
            if not pms.isAnonymousUser():
                member = pms.getAuthenticatedMember()
                adapter = getAdapter(member, ITwitterCredentialsProvider)
                if adapter is not None:
                    username, password = adapter.username(), adapter.password()
        if not username and not password:
            return False
        self.twitter = TwitterAPIAdapter(getUtility(ITwitterAPI), username, password)
        try:
            self.GetFriends(user=None)
        except HTTPError, e:
            if e.msg == 'Unauthorized':
                return False
            raise

        return True

    def linkify(self, text):
        return TEXT_URL_TO_ANCHOR.sub('<a href="\\g<1>">\\g<1></a>', text)

    def format_ago(self, atime, uppercase=False, invert=False):
        try:
            dt = DateTime(atime)
        except ValueError:
            return

        now = DateTime().toZone('GMT+0')
        now_secs = float(now)
        dt_secs = float(dt)
        if not invert:
            diff = now_secs - dt_secs
            if diff < 0:
                diff = 0
        else:
            diff = dt_secs - now_secs
            if diff <= 0:
                return
        ret = ''
        if diff < 3600:
            minutes = int(diff / 60)
            if minutes == 1:
                ret = _('1 minute')
            else:
                ret = _('%s minutes' % minutes)
        elif diff >= 3600 and diff < 86400:
            hours = int(diff / 3600)
            if hours == 1:
                ret = _('1 hour')
            else:
                ret = _('%s hours' % hours)
        elif diff >= 86400:
            days = int(diff / 86400)
            if days == 1:
                ret = _('1 day')
            else:
                ret = _('%s days' % days)
        if uppercase:
            return ret.upper()
        return ret

    def latest(self):
        result = self.twitter.GetUserTimeline(count=1)
        if result:
            return result[0]
        return

    @memoize.ram.cache(cache_key_60)
    def _GetFriendsTimeline(self, username, user=None, since=None):
        """
        Cacheable companion to GetFriendsTimeline
        """
        return self.twitter.GetFriendsTimeline(user=user, since=since)

    def GetFriendsTimeline(self, user=None, since=None):
        """
        This call is potentially too slow for normal use in ajax requests.
        The dashboard makes this call when it is first loaded, which provides
        an opportunity to use a memoize decorator.
        """
        return self._GetFriendsTimeline(username=self.twitter.username, user=user, since=since)

    @memoize.request.cache(lambda func, obj, user: (
     func.func_name, user), get_request='self.request')
    def GetFriends(self, user=None):
        return self.twitter.GetFriends(user=user)

    def getPluggableViewlets(self):
        manager = queryMultiAdapter((self.context, self.request, self), IViewletManager, name='collective.sylvester.dashboardmanager')
        viewlets = getAdapters((manager.context, manager.request, manager.__parent__, manager), IViewlet)
        return [ viewlet for (name, viewlet) in viewlets ]

    @errorhandler
    def __call__(self, *args, **kwargs):
        if not self.authenticate(redirect=True):
            return
        self.request.set('disable_border', 1)
        return super(SylvesterView, self).__call__(*args, **kwargs)


class CredentialsFormView(BrowserView):
    __module__ = __name__
    implements(ICredentialsFormView)

    def name(self):
        return self.__name__

    def submit(self, username, password, came_from=''):
        session = self.request.SESSION
        if not session.has_key('collective.sylvester.twitter'):
            session['collective.sylvester.twitter'] = {}
        session['collective.sylvester.twitter']['username'] = username
        session['collective.sylvester.twitter']['password'] = password
        getToolByName(self, 'plone_utils').addPortalMessage(_('Twitter credentials saved for this session'))
        if came_from:
            self.request.response.redirect(came_from)
        else:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            self.request.response.redirect(portal.absolute_url())

    def __call__(self, *args, **kwargs):
        form = self.request.form
        if form.has_key('submit'):
            return self.submit(form.get('username', ''), form.get('password', ''), form.get('came_from', ''))
        self.request.set('disable_border', 1)
        return super(CredentialsFormView, self).__call__(*args, **kwargs)


class PublishToTwitterFormView(BrowserView):
    __module__ = __name__
    implements(IPublishToTwitterFormView)

    def name(self):
        return self.__name__

    @errorhandler
    def submit(self, came_from=''):
        context = aq_inner(self.context)
        text = context.Description()
        if not text and HAS_STRIPOGRAM:
            if context.Schema().getField('text') is not None:
                text = html2text(context.getText())
        url_data = urlencode(dict(url=context.absolute_url()))
        try:
            link = urlopen('http://tinyurl.com/api-create.php', data=url_data).read().strip()
        except URLError:
            msg = 'An error was encountered while attempting to shorten the URL'
            getToolByName(self, 'plone_utils').addPortalMessage(_(msg), 'error')
            self.request.response.redirect(context.absolute_url())
            return

        text = text[:137 - len(link)]
        view = context.restrictedTraverse('@@collective.sylvester.dashboard')
        message = '%s...%s' % (text, link)
        view.twitter.PostUpdate(message, handle_error=False)
        getToolByName(self, 'plone_utils').addPortalMessage(_('Item published to twitter'))
        self.request.response.redirect(context.absolute_url())
        return

    def __call__(self, *args, **kwargs):
        form = self.request.form
        if form.has_key('submit'):
            return self.submit(form.get('came_from', ''))
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@collective.sylvester.dashboard')
        if not view.authenticate(redirect=True):
            return
        self.request.set('disable_border', 1)
        return super(PublishToTwitterFormView, self).__call__(*args, **kwargs)