# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/startapp.py
# Compiled at: 2019-02-14 00:35:17
from importlib import import_module
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand

class Command(TemplateCommand):
    help = 'Creates a Django app directory structure for the given app name in the current directory or optionally in the given directory.'
    missing_args_message = 'You must provide an application name.'

    def handle(self, **options):
        app_name, target = options.pop('name'), options.pop('directory')
        self.validate_name(app_name, 'app')
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError('%r conflicts with the name of an existing Python module and cannot be used as an app name. Please try another name.' % app_name)

        super(Command, self).handle('app', app_name, target, **options)