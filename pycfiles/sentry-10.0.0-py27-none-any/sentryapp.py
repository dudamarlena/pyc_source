# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/models/sentryapp.py
# Compiled at: 2019-09-04 11:06:02
from __future__ import absolute_import
import six, uuid, hmac, itertools, hashlib, re
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from hashlib import sha256
from sentry.constants import SentryAppStatus, SENTRY_APP_SLUG_MAX_LENGTH
from sentry.models import Organization
from sentry.models.apiscopes import HasApiScopes
from sentry.db.models import ArrayField, BoundedPositiveIntegerField, EncryptedJsonField, FlexibleForeignKey, ParanoidModel
EVENT_EXPANSION = {'issue': [
           'issue.created', 'issue.resolved', 'issue.ignored', 'issue.assigned'], 
   'error': [
           'error.created']}
VALID_EVENT_RESOURCES = ('issue', 'error')
REQUIRED_EVENT_PERMISSIONS = {'issue': 'event:read', 
   'error': 'event:read', 
   'project': 'project:read', 
   'member': 'member:read', 
   'organization': 'org:read', 
   'team': 'team:read'}
VALID_EVENTS = tuple(itertools.chain(*EVENT_EXPANSION.values()))

def default_uuid():
    return six.binary_type(uuid.uuid4())


class SentryApp(ParanoidModel, HasApiScopes):
    __core__ = True
    application = models.OneToOneField('sentry.ApiApplication', null=True, on_delete=models.SET_NULL, related_name='sentry_app')
    proxy_user = models.OneToOneField('sentry.User', null=True, on_delete=models.SET_NULL, related_name='sentry_app')
    owner = FlexibleForeignKey('sentry.Organization', related_name='owned_sentry_apps')
    name = models.TextField()
    slug = models.CharField(max_length=SENTRY_APP_SLUG_MAX_LENGTH, unique=True)
    author = models.TextField(null=True)
    status = BoundedPositiveIntegerField(default=SentryAppStatus.UNPUBLISHED, choices=SentryAppStatus.as_choices(), db_index=True)
    uuid = models.CharField(max_length=64, default=default_uuid)
    redirect_url = models.URLField(null=True)
    webhook_url = models.URLField(null=True)
    is_alertable = models.BooleanField(default=False)
    verify_install = models.BooleanField(default=True)
    events = ArrayField(of=models.TextField, null=True)
    overview = models.TextField(null=True)
    schema = EncryptedJsonField(default=dict)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_sentryapp'

    @classmethod
    def visible_for_user(cls, request):
        from sentry.auth.superuser import is_active_superuser
        if is_active_superuser(request):
            return cls.objects.all()
        return cls.objects.filter(status=SentryAppStatus.PUBLISHED)

    @property
    def organizations(self):
        if not self.pk:
            return Organization.objects.none()
        return Organization.objects.select_related('sentry_app_installations').filter(sentry_app_installations__sentry_app_id=self.id)

    @property
    def teams(self):
        from sentry.models import Team
        if not self.pk:
            return Team.objects.none()
        return Team.objects.filter(organization__in=self.organizations)

    @property
    def is_published(self):
        return self.status == SentryAppStatus.PUBLISHED

    @property
    def is_unpublished(self):
        return self.status == SentryAppStatus.UNPUBLISHED

    @property
    def is_internal(self):
        return self.status == SentryAppStatus.INTERNAL

    def save(self, *args, **kwargs):
        self._set_slug()
        self.date_updated = timezone.now()
        return super(SentryApp, self).save(*args, **kwargs)

    def is_installed_on(self, organization):
        return self.organizations.filter(pk=organization.pk).exists()

    def _set_slug(self):
        """
        Matches ``name``, but in lowercase, dash form.

        >>> self._set_slug('My Cool App')
        >>> self.slug
        my-cool-app
        """
        if not self.slug:
            self.slug = slugify(self.name)
        if self.is_internal and not self._has_internal_slug():
            self.slug = ('{}-{}').format(self.slug, hashlib.sha1(self.owner.slug).hexdigest()[0:6])

    def _has_internal_slug(self):
        return re.match('\\w+-[0-9a-zA-Z]+', self.slug)

    def build_signature(self, body):
        secret = self.application.client_secret
        return hmac.new(key=secret.encode('utf-8'), msg=body.encode('utf-8'), digestmod=sha256).hexdigest()