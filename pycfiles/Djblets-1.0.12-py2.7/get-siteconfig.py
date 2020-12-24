# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/siteconfig/management/commands/get-siteconfig.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.core.management.base import CommandError
from django.utils.translation import ugettext as _
from djblets.siteconfig.models import SiteConfiguration
from djblets.util.compat.django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Displays a setting in the site configuration."""

    def add_arguments(self, parser):
        """Add arguments to the command.

        Args:
            parser (object):
                The argument parser to add to.
        """
        parser.add_argument(b'--key', action=b'store', dest=b'key', help=_(b'The existing key to display (dot-separated)'))

    def handle(self, *args, **options):
        siteconfig = SiteConfiguration.objects.get_current()
        key = options[b'key']
        if key is None:
            raise CommandError(_(b'--key must be provided'))
        path = key.split(b'.')
        node = siteconfig.settings
        valid_key = True
        for item in path[:-1]:
            try:
                node = node[item]
            except KeyError:
                valid_key = False

        if valid_key:
            key_basename = path[(-1)]
            if key_basename not in node:
                valid_key = False
        if not valid_key:
            raise CommandError(_(b"'%s' is not a valid settings key") % key)
        value = node[key_basename]
        if value is None:
            value = b'null'
        elif isinstance(value, bool):
            if value:
                value = b'true'
            else:
                value = b'false'
        self.stdout.write(b'%s' % value)
        return