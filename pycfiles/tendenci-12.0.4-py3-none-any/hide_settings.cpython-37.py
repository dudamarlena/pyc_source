# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/site_settings/management/commands/hide_settings.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1630 bytes
from django.core.management.base import BaseCommand
from tendenci.apps.site_settings.models import Setting

class Command(BaseCommand):
    __doc__ = '\n    Update site settings in the database to not be client editable.\n    This was initially build to hide theme settings when switching themes.\n    '
    help = 'Hide settings (client_editable = false) in the site_settings_setting table'

    def add_arguments(self, parser):
        parser.add_argument('scope_category')

    def handle(self, scope_category, **options):
        if scope_category:
            settings = Setting.objects.filter(scope_category=scope_category)
            for setting in settings:
                try:
                    current_setting = Setting.objects.get(name=(setting.name),
                      scope=(setting.scope),
                      scope_category=(setting.scope_category))
                except:
                    current_setting = None

                print(current_setting)
                if current_setting:
                    current_setting.client_editable = False
                    current_setting.save()
                    print('%s (%s)  - hidden.' % (
                     setting.name,
                     setting.scope_category))