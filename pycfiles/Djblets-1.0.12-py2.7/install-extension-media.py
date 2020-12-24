# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/extensions/management/commands/install-extension-media.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from itertools import chain
from django.core.management.base import CommandError
from django.utils.translation import ugettext as _
from djblets.extensions.errors import InstallExtensionError, InvalidExtensionError
from djblets.extensions.manager import get_extension_managers
from djblets.util.compat.django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Install the extension media.

    This command will install the extension media for either a specific
    extension (specified with the ``--extension-id`` flag) or all installed
    extensions. Installation of the media can be forced (i.e., no version
    checking will be done.
    """

    def add_arguments(self, parser):
        """Add arguments to the command.

        Args:
            parser (object):
                The argument parser to add to.
        """
        parser.add_argument(b'--extension-id', dest=b'extension_id', default=None, help=_(b'An optional extension id'))
        parser.add_argument(b'--force', dest=b'force', action=b'store_true', default=False, help=_(b'Force installation of extension media'))
        return

    def handle(self, *args, **options):
        managers = get_extension_managers()
        force_install = options[b'force']
        if options[b'extension_id']:
            extensions = [self._find_extension(options[b'extension_id'], managers)]
        else:
            extensions = chain((extension, manager) for manager in managers for extension in manager.get_enabled_extensions())
        for extension, manager in extensions:
            try:
                manager.install_extension_media(extension, force_install)
            except InstallExtensionError as e:
                raise CommandError(b'Could not install extension media: %s' % e)

    def _find_extension(self, extension_id, managers):
        """Find an extension with the given ID in the managers.

        Args:
            extension_id (unicode):
                The extension's ID.

            managers (list):
                A list of :py:class:`~django.extensions.extension.Extension`
                classes (not instances).

        Returns:
            type:
            The specific :py:class:`~django.extensions.extension.Extension`
            class.
        """
        for manager in managers:
            try:
                return (
                 manager.get_enabled_extension(extension_id), manager)
            except InvalidExtensionError:
                pass

        raise CommandError(b'No such extension: %s' % extension_id)