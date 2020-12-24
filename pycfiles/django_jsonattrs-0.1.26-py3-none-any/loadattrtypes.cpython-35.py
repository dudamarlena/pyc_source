# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/management/commands/loadattrtypes.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 624 bytes
from django.core.management.base import BaseCommand
from jsonattrs.models import AttributeType, create_attribute_types

def run(force=False):
    if force:
        AttributeType.objects.all().delete()
    create_attribute_types()


class Command(BaseCommand):
    help = 'Load default attribute types.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', dest='force', default=False, help='Force object deletion and recreation')

    def handle(self, *args, **options):
        run(force=options['force'])