# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sessions/management/commands/clearsessions.py
# Compiled at: 2019-02-14 00:35:17
from importlib import import_module
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Can be run as a cronjob or directly to clean out expired sessions (only with the database backend at the moment).'

    def handle(self, **options):
        engine = import_module(settings.SESSION_ENGINE)
        try:
            engine.SessionStore.clear_expired()
        except NotImplementedError:
            self.stderr.write("Session engine '%s' doesn't support clearing expired sessions.\n" % settings.SESSION_ENGINE)