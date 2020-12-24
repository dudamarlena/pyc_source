# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/management/commands/clean_expired.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 642 bytes
""" Manifest Clean Expired Users Command
"""
try:
    import django.core.management.base as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()

class Command(BaseCommand):
    __doc__ = "\n    Search for users that still haven't verified their email after\n    ``MANIFEST_ACTIVATION_DAYS`` and delete them.\n\n    "
    help = 'Deletes expired users.'

    def handle(self, *args, **kwargs):
        USER_MODEL.objects.delete_expired_users()