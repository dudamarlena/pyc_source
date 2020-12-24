# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/diffsettings.py
# Compiled at: 2019-02-14 00:35:17
from django.core.management.base import BaseCommand

def module_to_dict(module, omittable=lambda k: k.startswith('_')):
    """Converts a module namespace to a Python dictionary."""
    return {k:repr(v) for k, v in module.__dict__.items() if not omittable(k)}


class Command(BaseCommand):
    help = 'Displays differences between the current settings.py and Django\'s\n    default settings. Settings that don\'t appear in the defaults are\n    followed by "###".'
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', dest='all', default=False, help='Display all settings, regardless of their value. Default values are prefixed by "###".')
        parser.add_argument('--default', dest='default', metavar='MODULE', default=None, help="The settings module to compare the current settings against. Leave empty to compare against Django's default settings.")
        return

    def handle(self, **options):
        from django.conf import settings, Settings, global_settings
        settings._setup()
        user_settings = module_to_dict(settings._wrapped)
        default = options['default']
        default_settings = module_to_dict(Settings(default) if default else global_settings)
        output = []
        for key in sorted(user_settings):
            if key not in default_settings:
                output.append('%s = %s  ###' % (key, user_settings[key]))
            elif user_settings[key] != default_settings[key]:
                output.append('%s = %s' % (key, user_settings[key]))
            elif options['all']:
                output.append('### %s = %s' % (key, user_settings[key]))

        return ('\n').join(output)