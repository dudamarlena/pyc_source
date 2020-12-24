# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-chameleon/chameleon/management/commands/starttheme.py
# Compiled at: 2013-01-07 06:27:52
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.importlib import import_module
import chameleon, os

class Command(TemplateCommand):
    help = 'Creates a pluggable django theme directory structure for the specified theme name in the current project.'

    def handle(self, app_name=None, target=None, **options):
        if app_name is None:
            raise CommandError('you must provide a theme name')
        options['template'] = options.get('template') or os.path.join(chameleon.__path__[0], 'conf', 'app_template')
        options['extensions'] += ['less', 'css']
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError('%r conflicts with the name of an existing Python module and cannot be used as a theme name. Please try another name.' % app_name)

        super(Command, self).handle('app', app_name, target, **options)
        return