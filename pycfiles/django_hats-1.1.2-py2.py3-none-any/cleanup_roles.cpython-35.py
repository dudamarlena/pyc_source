# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/management/commands/cleanup_roles.py
# Compiled at: 2017-01-18 10:34:43
# Size of source mod 2**32: 502 bytes
from django.core.management.base import BaseCommand
from django_hats.utils import cleanup_roles

class Command(BaseCommand):
    help = 'Removes stale Role Groups and Permissions from the database.'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        ret = cleanup_roles()
        if self.verbosity > 0:
            self.stdout.write('%(count)s roles removed' % {'count': ret[0]})