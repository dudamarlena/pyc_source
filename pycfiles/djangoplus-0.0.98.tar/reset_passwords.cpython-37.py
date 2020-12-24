# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/reset_passwords.py
# Compiled at: 2019-04-21 19:33:29
# Size of source mod 2**32: 361 bytes
from django.conf import settings
from django.core.management.base import BaseCommand
from djangoplus.admin.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.first()
        user.set_password(settings.DEFAULT_PASSWORD)
        User.objects.update(password=(user.password))