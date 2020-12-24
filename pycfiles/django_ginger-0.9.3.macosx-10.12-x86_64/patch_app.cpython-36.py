# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/patch_app.py
# Compiled at: 2015-05-20 12:21:43
# Size of source mod 2**32: 481 bytes
import optparse
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from ginger.meta import app

class Command(BaseCommand):
    args = 'app_name'
    help = 'Converts any app to standard ginger app with celery-tasks, forms, signals modules'

    def add_arguments(self, parser):
        parser.add_argument('app_name')

    def handle(self, **options):
        app_name = options['app_name']
        app.Application(app_name)