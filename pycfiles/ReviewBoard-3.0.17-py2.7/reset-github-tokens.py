# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/management/commands/reset-github-tokens.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import getpass
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.six.moves import input
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.errors import AuthorizationError, TwoFactorAuthCodeRequiredError
from reviewboard.hostingsvcs.models import HostingServiceAccount

class Command(BaseCommand):
    help = _(b'Resets associated GitHub tokens')
    option_list = BaseCommand.option_list + (
     make_option(b'--yes', action=b'store_true', default=False, dest=b'force_yes', help=_(b'Answer yes to all questions')),
     make_option(b'--local-sites', action=b'store', dest=b'local_sites', help=_(b'Comma-separated list of Local Sites to filter by')))

    def handle(self, *usernames, **options):
        force_yes = options[b'force_yes']
        local_sites = options[b'local_sites']
        accounts = HostingServiceAccount.objects.filter(service_name=b'github')
        if usernames:
            accounts = accounts.filter(username__in=usernames)
        if local_sites:
            local_site_names = local_sites.split(b',')
            if local_site_names:
                accounts = accounts.filter(local_site__name__in=local_site_names)
        for account in accounts:
            if force_yes:
                reset = b'y'
            else:
                if account.local_site:
                    reset_msg = _(b'Reset token for %(site_name)s (%(username)s) [Y/n] ') % {b'site_name': account.local_site.name, 
                       b'username': account.username}
                else:
                    reset_msg = _(b'Reset token for %s [Y/n] ') % account.username
                reset = input(reset_msg)
            if reset != b'n':
                self._reset_token(account)

    def _reset_token(self, account):
        service = account.service
        password = None
        auth_token = None
        while True:
            if not password and service.get_reset_auth_token_requires_password():
                password = getpass.getpass(_(b'Password for %s: ') % account.username)
                auth_token = None
            try:
                service.reset_auth_token(password, auth_token)
                self.stdout.write(_(b'Successfully reset token for %s\n') % account.username)
                break
            except TwoFactorAuthCodeRequiredError:
                auth_token = input(b'Enter your two-factor auth token: ')
            except AuthorizationError as e:
                self.stderr.write(b'%s\n' % e)
                password = None
            except Exception as e:
                self.stderr.write(_(b'Unexpected error: %s\n') % e)
                raise
                break

        return