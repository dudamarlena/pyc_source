# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/management/commands/deploy.py
# Compiled at: 2020-02-26 14:49:27
# Size of source mod 2**32: 532 bytes
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    __doc__ = '\n    Deploy a new version of Tendenci.\n    '

    def handle(self, *args, **options):
        call_command('collectstatic', '--link', '--noinput')
        call_command('update_settings')
        call_command('clear_theme_cache')
        call_command('populate_default_entity')
        call_command('populate_entity_and_auth_group_columns')
        call_command('loaddata', 'initial_data.json')