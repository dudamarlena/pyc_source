# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/bless_app.py
# Compiled at: 2015-01-10 11:41:10
import optparse
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from ginger.generators import views

class Command(BaseCommand):
    args = 'app_name'
    help = 'Converts any app to standard ginger app with celery-tasks, forms, signals modules'

    def handle(self, *args, **options):
        if not args:
            raise CommandError('No view has been given')
        if len(args) > 1:
            raise CommandError('Too many arguments. Check python manage.py help bless_app')
        app_name = args[0]
        views.GingerApp(app_name)