# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/sqlinitialdata.py
# Compiled at: 2018-07-11 18:15:30
from django.core.management.base import AppCommand, CommandError

class Command(AppCommand):
    help = "RENAMED: see 'sqlcustom'"

    def handle(self, *apps, **options):
        raise CommandError("This command has been renamed. Use the 'sqlcustom' command instead.")