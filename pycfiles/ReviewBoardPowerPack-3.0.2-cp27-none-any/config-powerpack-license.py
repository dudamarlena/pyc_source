# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/management/commands/config-powerpack-license.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import os
from optparse import make_option
from beanbag_licensing.auto_add import AutoAddMode
from beanbag_licensing.errors import IncorrectSignatureError
from beanbag_licensing.license import License
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from reviewboard.reviews.models import Group
from rbpowerpack.utils.extension import get_powerpack_extension

class Command(BaseCommand):
    """Allows the user to change Power Pack license settings.

    This gives users the ability to change the license settings and the
    license itself, to help with automation.
    """
    help = _(b'Configure the Power Pack license settings.')
    option_list = BaseCommand.option_list + (
     make_option(b'--auto-add-mode', dest=b'auto_add_mode', metavar=b'MODE', choices=[
      AutoAddMode.DISABLED,
      AutoAddMode.ALL_NEW,
      AutoAddMode.GROUPS], help=_(b'Whether to automatically add new users ("all-new"), users who join select groups ("groups"), or to disable auto-adding ("disabled").')),
     make_option(b'--auto-add-groups', metavar=b'GROUP_IDS', dest=b'auto_add_groups', help=_(b'Comma-separated list of groups whose new members should be auto-added to the license, if using --auto-add-mode=groups.')),
     make_option(b'--license-file', metavar=b'FILE', dest=b'license_file', help=_(b'New license file to install.')))

    def handle(self, **options):
        """Handle the configuration request.

        Args:
            options (dict):
                Options passed on the command line.
        """
        extension = get_powerpack_extension()
        if extension is None:
            raise CommandError(_(b'Power Pack is not enabled for this server.'))
        auto_add_mode = options[b'auto_add_mode']
        auto_add_groups = options[b'auto_add_groups']
        license_file = options[b'license_file']
        changed = False
        if auto_add_mode:
            extension.settings[b'auto_add_mode'] = auto_add_mode
            changed = True
        if auto_add_groups:
            if extension.settings.get(b'auto_add_mode') != AutoAddMode.GROUPS:
                raise CommandError(_(b'--auto-add-groups requires --auto-add-mode=groups.'))
            auto_add_groups = auto_add_groups.split(b',')
            groups = Group.objects.filter(name__in=auto_add_groups)
            if len(groups) != len(auto_add_groups):
                group_names = [ group.name for group in groups ]
                raise CommandError(_(b'The following group names are invalid: %s') % (b', ').join(set(auto_add_groups) - set(group_names)))
            extension.settings[b'auto_add_groups'] = [ group.pk for group in groups ]
            changed = True
        if license_file:
            license_file = os.path.expanduser(license_file)
            with open(license_file, b'r') as (fp):
                license_data = fp.read()
            try:
                License.read(license_data)
            except IncorrectSignatureError:
                raise CommandError(_(b'The license file "%s" is not a valid Power Pack license.') % license_file)

            extension.settings[b'license_data'] = license_data
            changed = True
        if changed:
            extension.settings.save()
        self.stdout.write(b'The license settings have been saved.\n')
        return