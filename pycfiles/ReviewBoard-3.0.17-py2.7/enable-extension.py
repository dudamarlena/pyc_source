# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/extensions/management/commands/enable-extension.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.errors import EnablingExtensionError, InvalidExtensionError
from reviewboard.extensions.base import get_extension_manager

class Command(BaseCommand):
    help = _(b'Enables an extension.')

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError(_(b'You must specify an extension ID to enable.'))
        extension_id = args[0]
        extension_mgr = get_extension_manager()
        try:
            extension_mgr.enable_extension(extension_id)
        except InvalidExtensionError:
            raise CommandError(_(b'%s is not a valid extension ID.') % extension_id)
        except EnablingExtensionError as e:
            raise CommandError(_(b'Error enabling extension: %(message)s\n\n%(error)s') % {b'message': e.message, 
               b'error': e.load_error})
        except Exception as e:
            raise CommandError(_(b'Unexpected error enabling extension: %s') % e)