# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/dbauthenticator.py
# Compiled at: 2012-10-12 07:02:39
from authenticator import Authenticator
from exception import CoilsException, AuthenticationException
from crypt import crypt

class DBAuthenticator(Authenticator):

    def __init__(self, context, metadata, options):
        Authenticator.__init__(self, context, metadata, options)

    def authenticate(self):
        if Authenticator.authenticate(self):
            return
        else:
            if self.debugging_enabled:
                self.log.debug(('Verifying database password for login "{0}".').format(self.login))
            secret = self.account.password
            if secret is None and self.account.object_id == 10000:
                self.log.warn('No password set for administrative account - permitted!')
                return True
            if secret is None:
                if self.debugging_enabled:
                    self.log.debug('NULL password encountered - denied.')
                raise AuthenticationException('Incorrect username or password')
            else:
                if secret == crypt(self.secret, secret[:2]):
                    if self.debugging_enabled:
                        self.log.debug('Password verified - approved.')
                    return True
                if self.debugging_enabled:
                    self.log.debug('Password incorrect - denied.')
                raise AuthenticationException('Incorrect username or password')
            return