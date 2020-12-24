# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/twine/twine/auth.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 2590 bytes
import warnings, getpass, functools
from typing import Optional, Callable
import keyring
from . import utils
from . import exceptions

class CredentialInput:

    def __init__(self, username: str=None, password: str=None):
        self.username = username
        self.password = password


class Resolver:

    def __init__(self, config: utils.RepositoryConfig, input: CredentialInput):
        self.config = config
        self.input = input

    @classmethod
    def choose(cls, interactive):
        if interactive:
            return cls
        else:
            return Private

    @property
    @functools.lru_cache()
    def username(self) -> Optional[str]:
        return utils.get_userpass_value((self.input.username),
          (self.config),
          key='username',
          prompt_strategy=(self.username_from_keyring_or_prompt))

    @property
    @functools.lru_cache()
    def password(self) -> Optional[str]:
        return utils.get_userpass_value((self.input.password),
          (self.config),
          key='password',
          prompt_strategy=(self.password_from_keyring_or_prompt))

    @property
    def system(self) -> Optional[str]:
        return self.config['repository']

    def get_username_from_keyring(self) -> Optional[str]:
        try:
            creds = keyring.get_credential(self.system, None)
            if creds:
                return creds.username
        except AttributeError:
            pass
        except Exception as exc:
            warnings.warn(str(exc))

    def get_password_from_keyring(self) -> Optional[str]:
        try:
            return keyring.get_password(self.system, self.username)
        except Exception as exc:
            warnings.warn(str(exc))

    def username_from_keyring_or_prompt(self) -> str:
        return self.get_username_from_keyring() or self.prompt('username', input)

    def password_from_keyring_or_prompt(self) -> str:
        return self.get_password_from_keyring() or self.prompt('password', getpass.getpass)

    def prompt(self, what: str, how: Callable) -> str:
        return how(f"Enter your {what}: ")


class Private(Resolver):

    def prompt(self, what: str, how: Optional[Callable]=None) -> str:
        raise exceptions.NonInteractive(f"Credential not found for {what}.")