# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/runfcgi.py
# Compiled at: 2018-07-11 18:15:30
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs this project as a FastCGI application. Requires flup.'
    args = '[various KEY=val options, use `runfcgi help` for help]'

    def handle(self, *args, **options):
        from django.conf import settings
        from django.utils import translation
        try:
            translation.activate(settings.LANGUAGE_CODE)
        except AttributeError:
            pass

        from django.core.servers.fastcgi import runfastcgi
        runfastcgi(args)

    def usage(self, subcommand):
        from django.core.servers.fastcgi import FASTCGI_HELP
        return FASTCGI_HELP