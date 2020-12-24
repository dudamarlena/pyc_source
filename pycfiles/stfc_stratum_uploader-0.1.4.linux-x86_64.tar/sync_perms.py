# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/custom_auth/management/commands/sync_perms.py
# Compiled at: 2013-08-08 04:50:11
from django.core.management.base import BaseCommand
from django.db.models import get_models, get_app
from django.contrib.auth.management import create_permissions

class Command(BaseCommand):
    args = '<app app ...>'
    help = 'reloads permissions for specified apps, or all apps if no args are specified'

    def handle(self, *args, **options):
        if not args:
            apps = []
            for model in get_models():
                apps.append(get_app(model._meta.app_label))

        else:
            apps = []
            for arg in args:
                apps.append(get_app(arg))

            for app in apps:
                create_permissions(app, get_models(), options.get('verbosity', 0))