# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme_editor/management/commands/set_theme.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1091 bytes
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    __doc__ = '\n    Example: python manage.py set_theme thinksmart\n    '

    def add_arguments(self, parser):
        parser.add_argument('theme_name')

    def handle(self, theme_name, **options):
        """
        Set the website theme via theme name
        """
        from tendenci.apps.site_settings.models import Setting
        try:
            setting = Setting.objects.get(name='theme',
              scope='module',
              scope_category='theme_editor')
            setting.set_value(theme_name)
            setting.save()
            call_command('hide_settings', 'theme')
            call_command('update_settings', 'themes.%s' % theme_name.lstrip())
            call_command('clear_cache')
        except Setting.DoesNotExist:
            if int(options['verbosity']) > 0:
                print('We could not update the theme because the setting or theme is not available.')