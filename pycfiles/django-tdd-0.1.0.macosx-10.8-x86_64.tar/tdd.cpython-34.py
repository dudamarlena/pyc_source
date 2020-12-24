# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kevin/workspace/Django_TDD/lib/python3.4/site-packages/django_tdd/management/commands/tdd.py
# Compiled at: 2014-04-11 16:50:05
# Size of source mod 2**32: 385 bytes
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *apps, **options):
        from django.core.management import call_command
        from django.conf import settings
        settings.ALLOWED_HOSTS += 'localhost'
        call_command('test')
        call_command('runserver')