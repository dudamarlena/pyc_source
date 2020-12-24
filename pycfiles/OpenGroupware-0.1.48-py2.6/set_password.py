# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/set_password.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import Contact
from crypt import crypt
import random

class SetPassword(Command):
    __domain__ = 'account'
    __operation__ = 'set-password'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        self.password = params.get('password', None)
        self.login = params.get('login', self._ctx.get_login())
        return

    def generate_salt(self):
        salt = ''
        while len(salt) < 2:
            i = random.randrange(1024)
            if i < 257:
                x = chr(random.randrange(256))
                if x.isalnum():
                    salt = ('{0}{1}').format(salt, x)

        return salt

    def run(self, **params):
        self._result = False
        if self.password is None:
            raise CoilsException('No password specified')
        db = self._ctx.db_session()
        query = db.query(Contact).filter(and_(Contact.login == self.login, Contact.is_account == 1, Contact.status != 'archived'))
        data = query.all()
        if len(data) > 1:
            raise AuthenticationException('Multiple accounts match criteria!')
        elif len(data) == 0:
            self.log.error(('No such account as {0}.').format(self.login))
            raise CoilsException(('No such account as {0}.').format(self.login))
        else:
            account = data[0]
            account.password = crypt(self.password, self.generate_salt())
            self._result = True
        return