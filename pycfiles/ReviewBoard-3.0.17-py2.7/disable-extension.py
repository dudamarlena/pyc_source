# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/extensions/management/commands/disable-extension.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import get_extension_manager

class Command(BaseCommand):
    help = _(b'Disables an extension.')

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError(_(b'You must specify an extension ID to disable.'))
        extension_id = args[0]
        extension_mgr = get_extension_manager()
        try:
            extension_mgr.disable_extension(extension_id)
        except Exception as e:
            raise CommandError(_(b'Unexpected error disabling extension: %s') % e)