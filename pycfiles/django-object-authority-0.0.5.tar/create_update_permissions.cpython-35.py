# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/management/commands/create_update_permissions.py
# Compiled at: 2017-05-31 09:11:55
# Size of source mod 2**32: 1860 bytes
from django.core.management.base import BaseCommand
from django_object_authority.utils import create_update_permissions
APPS = 'applications'
MODELS = 'models'
PERMISSIONS = 'permissions'

class Command(BaseCommand):
    help = 'Utility to create or update all required permissions to manage the app.'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--applications', nargs='+', type=str, dest=APPS, default=None, help='List of applications to create permissions of all their models.')
        parser.add_argument('-m', '--models', nargs='+', type=str, dest=MODELS, default=None, help='List of models to create permissions.')
        parser.add_argument('-n', '--new', nargs='+', type=str, dest=PERMISSIONS, default=None, help='List of new permission labels.')

    def handle(self, *args, **options):
        self.initialize(options)
        self.create_update_permissions()
        self.stdout.write(self.style.SUCCESS('Permission creation has successfully finished!'))

    def initialize(self, options):
        """Set all options as instance attribute."""
        for key, value in options.items():
            setattr(self, key, value)

    def create_update_permissions(self):
        """Create permissions for all available application models."""
        self.stdout.write('Creating permissions...')
        created_perm, updated_perm = create_update_permissions(applications=getattr(self, APPS), models=getattr(self, MODELS), permissions=getattr(self, PERMISSIONS))
        self.stdout.write('There are {} new permission and ignore {} because they already exist!'.format(created_perm, updated_perm))