# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/cleanup.py
# Compiled at: 2018-07-11 18:15:30
import warnings
from django.contrib.sessions.management.commands import clearsessions

class Command(clearsessions.Command):

    def handle_noargs(self, **options):
        warnings.warn('The `cleanup` command has been deprecated in favor of `clearsessions`.', PendingDeprecationWarning)
        super(Command, self).handle_noargs(**options)