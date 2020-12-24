# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Development/django-shell/shell_plus/management/commands/shell+.py
# Compiled at: 2015-07-27 21:22:57
import datetime, os
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.cache import cache
from django.core.urlresolvers import resolve, reverse

class Command(NoArgsCommand):
    help = 'Runs a Python interactive interpreter.'
    requires_system_checks = True

    def handle_noargs(self, **options):
        from django.apps import apps
        loaded_models = apps.get_models()
        import code
        imported_objects = {'datetime': datetime, 
           'cache': cache, 
           'reverse': reverse, 
           'resolve': resolve, 
           'settings': settings}
        for model in loaded_models:
            imported_objects[model.__name__] = model

        try:
            import readline
        except ImportError:
            pass
        else:
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
            readline.parse_and_bind('tab:complete')

        pythonrc = os.environ.get('PYTHONSTARTUP')
        if pythonrc and os.path.isfile(pythonrc):
            try:
                execfile(pythonrc)
            except NameError:
                pass

        import user
        code.interact(local=imported_objects)