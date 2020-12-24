# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\django-test-cms-new\management\commands\fix_permissions.py
# Compiled at: 2019-05-23 09:51:50
import sys
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Fix permissions for proxy models.'

    def handle(self, *args, **options):
        for model in apps.get_models():
            opts = model._meta
            sys.stdout.write(('{}-{}\n').format(opts.app_label, opts.object_name.lower()))
            ctype, created = ContentType.objects.get_or_create(app_label=opts.app_label, model=opts.object_name.lower())
            for codename, name in _get_all_permissions(opts):
                sys.stdout.write(('  --{}\n').format(codename))
                p, created = Permission.objects.get_or_create(codename=codename, content_type=ctype, defaults={'name': name})
                if created:
                    sys.stdout.write(('Adding permission {}\n').format(p))