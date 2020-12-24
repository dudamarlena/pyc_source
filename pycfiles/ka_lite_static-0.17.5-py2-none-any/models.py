# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/models.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import hmac, time
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from tastypie.utils import now
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha

@python_2_unicode_compatible
class ApiAccess(models.Model):
    """A simple model for use with the ``CacheDBThrottle`` behaviors."""
    identifier = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, default=b'')
    request_method = models.CharField(max_length=10, blank=True, default=b'')
    accessed = models.PositiveIntegerField()

    def __str__(self):
        return b'%s @ %s' % (self.identifier, self.accessed)

    def save(self, *args, **kwargs):
        self.accessed = int(time.time())
        return super(ApiAccess, self).save(*args, **kwargs)


if b'django.contrib.auth' in settings.INSTALLED_APPS:
    import uuid
    from tastypie.compat import AUTH_USER_MODEL

    class ApiKey(models.Model):
        user = models.OneToOneField(AUTH_USER_MODEL, related_name=b'api_key')
        key = models.CharField(max_length=128, blank=True, default=b'', db_index=True)
        created = models.DateTimeField(default=now)

        def __unicode__(self):
            return b'%s for %s' % (self.key, self.user)

        def save(self, *args, **kwargs):
            if not self.key:
                self.key = self.generate_key()
            return super(ApiKey, self).save(*args, **kwargs)

        def generate_key(self):
            new_uuid = uuid.uuid4()
            return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()

        class Meta:
            abstract = getattr(settings, b'TASTYPIE_ABSTRACT_APIKEY', False)


    def create_api_key(sender, **kwargs):
        """
        A signal for hooking up automatic ``ApiKey`` creation.
        """
        if kwargs.get(b'created') is True:
            ApiKey.objects.create(user=kwargs.get(b'instance'))