# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/models.py
# Compiled at: 2015-12-28 07:24:57
from httplib import HTTPConnection
from datetime import datetime, timedelta
from urlparse import parse_qs
from django.db import models
import jsonfield
from django.utils.translation import ugettext as _
from fandjango.utils import cached_property as cached
from fandjango.settings import FACEBOOK_APPLICATION_ID, FACEBOOK_APPLICATION_SECRET_KEY
from facepy import GraphAPI
import requests
try:
    from django.utils.timezone import now
except ImportError:

    def now():
        return datetime.now()


class Facebook:
    """
    Facebook instances hold information on the current user and
    his/her signed request.
    """
    user = None
    signed_request = None
    oauth_token = None


class User(models.Model):
    """
    Instances of the User class represent Facebook users who
    have authorized the application.
    """
    facebook_id = models.BigIntegerField(_('facebook id'), unique=True)
    facebook_username = models.CharField(_('facebook username'), max_length=255, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(_('middle name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    email = models.CharField(_('email'), max_length=255, blank=True, null=True)
    locale = models.CharField(_('locale'), max_length=255, blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=255, blank=True, null=True)
    authorized = models.BooleanField(_('authorized'), default=True)
    oauth_token = models.OneToOneField('OAuthToken', verbose_name=_('OAuth token'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_seen_at = models.DateTimeField(_('last seen at'), auto_now_add=True)
    extra_data = jsonfield.JSONField()

    @property
    def full_name(self):
        """Return the user's first name."""
        if self.first_name and self.middle_name and self.last_name:
            return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)

    @property
    @cached(days=30)
    def picture(self):
        """
        A string describing the URL to the user's profile picture.
        """
        return requests.get('http://graph.facebook.com/%s/picture' % self.facebook_id).url

    @property
    def permissions(self):
        """
        A list of strings describing `permissions`_ the user has granted your application.

        .. _permissions: http://developers.facebook.com/docs/reference/api/permissions/
        """
        records = self.graph.get('me/permissions')['data']
        permissions = []
        for record in records:
            if record['status'] == 'granted':
                permissions.append(record['permission'])

        return permissions

    @property
    def graph(self):
        """
        A ``Facepy.GraphAPI`` instance initialized with the user's access token (See `Facepy`_).

        .. _Facepy: http://github.com/jgorset/facepy
        """
        return GraphAPI(self.oauth_token.token)

    def synchronize(self, graph_data=None):
        """
        Synchronize ``facebook_username``, ``first_name``, ``middle_name``,
        ``last_name`` and ``birthday`` with Facebook.

        :param graph_data: Optional pre-fetched graph data
        """
        profile = graph_data or self.graph.get('me')
        self.facebook_username = profile.get('username')
        self.first_name = profile.get('first_name')
        self.middle_name = profile.get('middle_name')
        self.last_name = profile.get('last_name')
        self.birthday = datetime.strptime(profile['birthday'], '%m/%d/%Y') if profile.has_key('birthday') else None
        self.email = profile.get('email')
        self.locale = profile.get('locale')
        self.gender = profile.get('gender')
        self.extra_data = profile
        self.save()
        return

    def __unicode__(self):
        if self.full_name:
            return '%s' % self.full_name
        else:
            if self.facebook_username:
                return '%s' % self.facebook_username
            return '%s' % self.facebook_id

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OAuthToken(models.Model):
    """
    Instances of the OAuthToken class are credentials used to query
    the Facebook API on behalf of a user.
    """
    token = models.TextField(_('token'))
    issued_at = models.DateTimeField(_('issued at'))
    expires_at = models.DateTimeField(_('expires at'), null=True, blank=True)

    @property
    def expired(self):
        """Determine whether the OAuth token has expired."""
        if self.expires_at:
            return self.expires_at < now()
        return False

    @property
    def extended(self):
        """Determine whether the OAuth token has been extended."""
        if self.expires_at:
            return self.expires_at - self.issued_at > timedelta(days=30)
        else:
            return False

    def extend(self):
        """Extend the OAuth token."""
        graph = GraphAPI()
        response = graph.get('oauth/access_token', client_id=FACEBOOK_APPLICATION_ID, client_secret=FACEBOOK_APPLICATION_SECRET_KEY, grant_type='fb_exchange_token', fb_exchange_token=self.token)
        components = parse_qs(response)
        self.token = components['access_token'][0]
        self.expires_at = now() + timedelta(seconds=int(components['expires'][0]))
        self.save()

    class Meta:
        verbose_name = _('OAuth token')
        verbose_name_plural = _('OAuth tokens')