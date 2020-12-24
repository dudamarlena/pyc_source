# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/diffsettings.py
# Compiled at: 2018-07-11 18:15:30
from django.core.management.base import NoArgsCommand

def module_to_dict(module, omittable=lambda k: k.startswith('_')):
    """Converts a module namespace to a Python dictionary. Used by get_settings_diff."""
    return dict([ (k, repr(v)) for k, v in module.__dict__.items() if not omittable(k) ])


class Command(NoArgsCommand):
    help = 'Displays differences between the current settings.py and Django\'s\n    default settings. Settings that don\'t appear in the defaults are\n    followed by "###".'
    requires_model_validation = False

    def handle_noargs(self, **options):
        from django.conf import settings, global_settings
        settings._setup()
        user_settings = module_to_dict(settings._wrapped)
        default_settings = module_to_dict(global_settings)
        output = []
        for key in sorted(user_settings.keys()):
            if key not in default_settings:
                output.append('%s = %s  ###' % (key, user_settings[key]))
            elif user_settings[key] != default_settings[key]:
                output.append('%s = %s' % (key, user_settings[key]))

        return ('\n').join(output)