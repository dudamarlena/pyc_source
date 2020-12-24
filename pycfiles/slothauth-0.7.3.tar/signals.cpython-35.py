# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/signals.py
# Compiled at: 2017-08-16 16:41:40
# Size of source mod 2**32: 409 bytes
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .utils import disable_for_loaddata
from . import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@disable_for_loaddata
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)