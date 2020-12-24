# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/src/django-rest-framework-jwt-refresh-token/refreshtoken/models.py
# Compiled at: 2016-01-28 09:27:04
# Size of source mod 2**32: 1424 bytes
import binascii, os
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

@python_2_unicode_compatible
class RefreshToken(models.Model):
    __doc__ = '\n    Copied from\n    https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/models.py\n    Wanted to only change the user relation to be a "ForeignKey" instead of a OneToOneField\n\n    The `ForeignKey` value allows us to create multiple RefreshTokens per user\n\n    '
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='refresh_tokens')
    app = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'app')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(RefreshToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key