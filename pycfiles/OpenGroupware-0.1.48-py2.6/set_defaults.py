# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/set_defaults.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class SetDefaults(Command):
    __domain__ = 'account'
    __operation__ = 'set-defaults'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        self.login = None
        if 'defaults' in params:
            self.defaults = params('defaults')
        else:
            raise CoilsException(('No defaults provided to {0}').format(self.command_name()))
        if 'id' in params or 'login' in params:
            if 'id' in params:
                self.account_id = int(params['id'])
            else:
                self.login = params['login']
        else:
            self.account_id = self._ctx.account_id
        return

    def run(self):
        self._result = None
        if self.login is not None:
            account = self._ctx.run_command('account::get', login=self.login)
            if account is None:
                raise CoilsException(('{0} unable to resolve login {1}').format(self.command_name(), self.login))
            self.account_id = account.object_id
        if account.object_id not in self._ctx.context_ids or self._ctx.account_id > 10000:
            raise CoilsException(('Account {0} not permitted to modify defaults of account {1}').format(self._ctx.account_id, self.account_id))
        ud = UserDefaultsManager(self.account_id)
        ud.update_defaults(self.defaults)
        ud.sync()
        return