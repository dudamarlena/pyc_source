# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/management/commands/initial_migrate.py
# Compiled at: 2020-02-26 14:49:27
# Size of source mod 2**32: 407 bytes
import django.core.management.commands.migrate as MigrateCommand

class Command(MigrateCommand):
    requires_system_checks = False