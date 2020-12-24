# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/credentials.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1355 bytes
import os, abc
from .py27compat import add_metaclass

@add_metaclass(abc.ABCMeta)
class Credential(object):
    __doc__ = 'Abstract class to manage credentials\n    '

    @abc.abstractproperty
    def username(self):
        pass

    @abc.abstractproperty
    def password(self):
        pass


class SimpleCredential(Credential):
    __doc__ = 'Simple credentials implementation\n    '

    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


class EnvironCredential(Credential):
    __doc__ = 'Source credentials from environment variables.\n       Actual sourcing is deferred until requested.\n    '

    def __init__(self, user_env_var, pwd_env_var):
        self.user_env_var = user_env_var
        self.pwd_env_var = pwd_env_var

    def _get_env(self, env_var):
        """Helper to read an environment variable
        """
        value = os.environ.get(env_var)
        if not value:
            raise ValueError('Missing environment variable:%s' % env_var)
        return value

    @property
    def username(self):
        return self._get_env(self.user_env_var)

    @property
    def password(self):
        return self._get_env(self.pwd_env_var)