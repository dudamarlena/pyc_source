# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/sync_roles.py
# Compiled at: 2019-04-02 21:11:59
# Size of source mod 2**32: 461 bytes
from django.core.management.base import BaseCommand
from djangoplus.admin.models import User, Role
from djangoplus.cache import CACHE

class Command(BaseCommand):

    def handle(self, *args, **options):
        Role.objects.all().delete()
        for cls in CACHE['ROLE_MODELS']:
            for o in cls.objects.all():
                o.save()

        User.objects.filter(role__group__isnull=True).exclude(is_superuser=True).delete()