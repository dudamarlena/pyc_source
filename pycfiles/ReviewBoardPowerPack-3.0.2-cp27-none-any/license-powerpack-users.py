# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/management/commands/license-powerpack-users.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from beanbag_licensing.errors import TooManyUsersForLicenseError
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from rbpowerpack.utils.extension import get_powerpack_extension

class Command(BaseCommand):
    help = b'Add one or more users to the Power Pack license.'

    def handle(self, *usernames, **options):
        extension = get_powerpack_extension()
        if extension is None:
            raise CommandError(_(b'Power Pack is not enabled for this server.'))
        if not usernames:
            raise CommandError(_(b'One or more usernames must be provided.'))
        users = User.objects.filter(username__in=usernames)
        if len(users) != len(usernames):
            missing_users = set(usernames) - set(user.username for user in users)
            raise CommandError(_(b'The following username(s) were not found: %s') % (
             (b', ').join(missing_users),))
        license_settings = extension.license_settings
        licensed_usernames = [ user.username for user in users if license_settings.is_user_licensed(user)
                             ]
        if licensed_usernames:
            self.stderr.write(b'The following user(s) are already licensed: %s\n' % (b', ').join(licensed_usernames))
        try:
            licensed_users = license_settings.add_licensed_users(users)
        except TooManyUsersForLicenseError as e:
            raise CommandError(e)

        self.stdout.write(b'%d user(s) added to the license.\n' % len(licensed_users))
        return