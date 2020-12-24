# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/gittle/auth.py
# Compiled at: 2013-09-03 02:36:01
import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

from .exceptions import InvalidRSAKey
__all__ = ('GittleAuth', )

def get_pkey_file(pkey):
    if isinstance(pkey, basestring):
        if os.path.exists(pkey):
            pkey_file = open(pkey)
        else:
            pkey_file = StringIO(pkey)
    else:
        return pkey
    return pkey_file


class GittleAuth(object):
    KWARG_KEYS = ('username', 'password', 'pkey', 'look_for_keys', 'allow_agent')

    def __init__(self, username=None, password=None, pkey=None, look_for_keys=None, allow_agent=None):
        self.username = username
        self.password = password
        self.allow_agent = allow_agent
        self.look_for_keys = look_for_keys
        self.pkey = self.setup_pkey(pkey)

    def setup_pkey(self, pkey):
        pkey_file = get_pkey_file(pkey)
        if not pkey_file:
            return
        else:
            if HAS_PARAMIKO:
                return paramiko.RSAKey.from_private_key(pkey_file)
            raise InvalidRSAKey('Requires paramiko to build RSA key')
            return

    @property
    def can_password(self):
        return self.username and self.password

    @property
    def can_pkey(self):
        return self.pkey is not None

    @property
    def could_other(self):
        return self.look_for_keys or self.allow_agent

    def can_auth(self):
        return any([
         self.can_password,
         self.can_pkey,
         self.could_other])

    def kwargs(self):
        kwargs = {key:getattr(self, key) for key in self.KWARG_KEYS if getattr(self, key, None)}
        return kwargs