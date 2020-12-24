# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/opt/.virtualenvs/teste123/lib/python3.6/site-packages/djangoplus/admin/management/commands/sync.py
# Compiled at: 2018-04-15 13:18:44
# Size of source mod 2**32: 1534 bytes
import os
from djangoplus.conf import base_settings
from django.conf import settings
from django.core import serializers
from django.utils import termcolors
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

def print_and_call(command, *args, **kwargs):
    kwargs.setdefault('interactive', True)
    print(termcolors.make_style(fg='cyan', opts=('bold', ))('>>> {} {}{}'.format(command, ' '.join(args), ' '.join(['{}={}'.format(k, v) for k, v in list(kwargs.items())]))))
    call_command(command, *args, **kwargs)


class Command(BaseCommand):

    def handle(self, *args, **options):
        app_labels = []
        for app_label in settings.INSTALLED_APPS:
            if app_label not in base_settings.INSTALLED_APPS and '.' not in app_label:
                app_labels.append(app_label)

        print_and_call(*('makemigrations', ), *app_labels)
        print_and_call('migrate')
        User = get_user_model()
        if not User.objects.exists():
            user = User.objects.create_superuser(settings.DEFAULT_SUPERUSER, None, settings.DEFAULT_PASSWORD)
            user.name = 'Admin'
            user.save()
        if os.path.exists(os.path.join(settings.BASE_DIR, 'logs')):
            print_and_call('collectstatic', clear=True, verbosity=0, interactive=False)