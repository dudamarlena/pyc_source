# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/projects/django-init/django_init/management/commands/project.py
# Compiled at: 2020-01-15 01:44:42
# Size of source mod 2**32: 1314 bytes
from django.core.management.base import BaseCommand
from django_init.management import add_arguments
from django_init.apps.app import AppsManagement

class Command(BaseCommand):
    help = 'Creates a Django project directory structure for the given project name in the current directory or optionally in the given directory.'

    def add_arguments(self, parser):
        parser.add_argument('command_name', help='Name of command')
        parser.add_argument('project_name', nargs='?', help='Name of project')

    def handle(self, *args, **options):
        print(options)
        app = AppsManagement()
        project_name = options.get('project_name')
        if project_name:
            if project_name == 'base':
                app.create_project()
                app.create_app('logs')
                app.create_app('common')
                app.create_app('config')
                app.create_app('menus')
                app.create_app('seo')
                app.create_app('accounts')
                app.create_app('feedback')
                app.create_app('templates')
            else:
                print('Unknown name of command: %r' % project_name)
        else:
            app.create_project()