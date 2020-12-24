# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/management/commands/testserver.py
# Compiled at: 2018-07-11 18:15:31
from django.core.management.commands import testserver
from south.management.commands import patch_for_test_db_setup

class Command(testserver.Command):

    def handle(self, *args, **kwargs):
        patch_for_test_db_setup()
        super(Command, self).handle(*args, **kwargs)