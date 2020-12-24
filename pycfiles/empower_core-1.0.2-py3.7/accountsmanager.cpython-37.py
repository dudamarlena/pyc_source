# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/accountsmanager/accountsmanager.py
# Compiled at: 2020-05-10 06:48:30
# Size of source mod 2**32: 3554 bytes
"""Accounts manager."""
from empower_core.service import EService
from empower_core.accountsmanager.account import Account
from empower_core.accountsmanager.accountshandler import AccountsHandler

class AccountsManager(EService):
    __doc__ = 'Accounts manager.'
    HANDLERS = [
     AccountsHandler]
    ACCOUNT_IMPL = Account
    accounts = {}

    def start(self):
        super().start()
        for account in self.ACCOUNT_IMPL.objects.all():
            self.accounts[account.username] = account

        if 'root' not in self.accounts:
            self.log.info('No root user found, creating defaults!')
            self.create(username='root', password='root',
              name='admin',
              email='admin@5g-empower.io')
            self.create(username='foo', password='foo',
              name='Foo',
              email='foo@5g-empower.io')
            self.create(username='bar', password='bar',
              name='Bar',
              email='bar@5g-empower.io')

    def check_permission(self, username, password):
        """Check if username/password match."""
        if username not in self.accounts:
            return False
        if self.accounts[username].password != password:
            return False
        return True

    def create(self, username, name, email, password):
        """Create new account."""
        if username in self.accounts:
            raise ValueError('Duplicate username %s found' % username)
        user = self.ACCOUNT_IMPL(username=username, password=password,
          name=name,
          email=email)
        user.save()
        self.accounts[username] = user
        return self.accounts[username]

    def update(self, username, name, email, password=None):
        """Update account."""
        if username not in self.accounts:
            raise KeyError('Username %s not found' % username)
        user = self.accounts[username]
        try:
            user.name = name
            user.email = email
            if password:
                user.password = password
            user.save()
        finally:
            user.refresh_from_db()

        return self.accounts[username]

    def remove(self, username):
        """Check if username/password match."""
        if username == 'root':
            raise ValueError("The 'root' account cannot be removed")
        if username not in self.accounts:
            raise KeyError('Username %s not found' % username)
        user = self.accounts[username]
        user.delete()
        del self.accounts[username]


def launch(context, service_id):
    """ Initialize the module. """
    return AccountsManager(context=context, service_id=service_id)