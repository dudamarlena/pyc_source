# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/startproject.py
# Compiled at: 2018-07-11 18:15:30
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.crypto import get_random_string
from django.utils.importlib import import_module

class Command(TemplateCommand):
    help = 'Creates a Django project directory structure for the given project name in the current directory or optionally in the given directory.'

    def handle(self, project_name=None, target=None, *args, **options):
        if project_name is None:
            raise CommandError('you must provide a project name')
        try:
            import_module(project_name)
        except ImportError:
            pass
        else:
            raise CommandError('%r conflicts with the name of an existing Python module and cannot be used as a project name. Please try another name.' % project_name)

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        options['secret_key'] = get_random_string(50, chars)
        super(Command, self).handle('project', project_name, target, **options)
        return