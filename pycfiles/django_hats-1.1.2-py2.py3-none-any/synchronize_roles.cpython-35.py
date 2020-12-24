# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/management/commands/synchronize_roles.py
# Compiled at: 2017-01-18 10:50:36
# Size of source mod 2**32: 827 bytes
from django.core.management.base import BaseCommand
from django_hats.apps import DjangoHatsConfig
from django_hats.bootstrap import Bootstrapper
from django_hats.signals import post_synchronize_roles
from django_hats.utils import synchronize_roles

class Command(BaseCommand):
    help = 'Synchronizes Role Groups and Permissions with the database.'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        roles = Bootstrapper.get_roles()
        synchronize_roles(roles)
        post_synchronize_roles.send(sender=DjangoHatsConfig)
        if self.verbosity > 0:
            self.stdout.write('Role synchronization complete.')