# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/management/commands/resolve-check.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import sys
from django.core.management.base import BaseCommand, CommandError
from djblets.siteconfig.models import SiteConfiguration

class Command(BaseCommand):
    """Management command to manually update the state of an update check."""
    help = b'Resolves a manual update check'

    def handle(self, *args, **options):
        """Handle the command."""
        if len(args) != 1:
            self.stderr.write(b'You must specify a check to resolve')
            sys.exit(1)
        check_name = args[0]
        siteconfig = SiteConfiguration.objects.get_current()
        updates = siteconfig.settings.get(b'manual-updates', {})
        if check_name not in updates:
            raise CommandError(b"Couldn't find manual update check '%s'\n" % check_name)
        if updates[check_name]:
            self.stdout.write(b"Already resolved manual update check '%s'" % check_name)
        else:
            updates[check_name] = True
            siteconfig.save()
            self.stdout.write(b"Resolved manual update check '%s'" % check_name)