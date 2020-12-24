# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/backends/Windows.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 6055 bytes
import functools
from ..util import properties
from ..backend import KeyringBackend
from ..credentials import SimpleCredential
from ..errors import PasswordDeleteError, ExceptionRaisedContext
with ExceptionRaisedContext() as (missing_deps):
    try:
        from win32ctypes.pywin32 import pywintypes
        from win32ctypes.pywin32 import win32cred
        win32cred.__name__
    except ImportError:
        import pywintypes, win32cred
        win32cred.__name__

__metaclass__ = type

class Persistence:

    def __get__(self, keyring, type=None):
        return getattr(keyring, '_persist', win32cred.CRED_PERSIST_ENTERPRISE)

    def __set__(self, keyring, value):
        """
        Set the persistence value on the Keyring. Value may be
        one of the win32cred.CRED_PERSIST_* constants or a
        string representing one of those constants. For example,
        'local machine' or 'session'.
        """
        if isinstance(value, str):
            attr = 'CRED_PERSIST_' + value.replace(' ', '_').upper()
            value = getattr(win32cred, attr)
        setattr(keyring, '_persist', value)


class WinVaultKeyring(KeyringBackend):
    __doc__ = "\n    WinVaultKeyring stores encrypted passwords using the Windows Credential\n    Manager.\n\n    Requires pywin32\n\n    This backend does some gymnastics to simulate multi-user support,\n    which WinVault doesn't support natively. See\n    https://bitbucket.org/kang/python-keyring-lib/issue/47/winvaultkeyring-only-ever-returns-last#comment-731977\n    for details on the implementation, but here's the gist:\n\n    Passwords are stored under the service name unless there is a collision\n    (another password with the same service name but different user name),\n    in which case the previous password is moved into a compound name:\n    {username}@{service}\n    "
    persist = Persistence()

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        If available, the preferred backend on Windows.
        """
        if missing_deps:
            raise RuntimeError('Requires Windows and pywin32')
        return 5

    @staticmethod
    def _compound_name(username, service):
        return '%(username)s@%(service)s' % vars()

    def get_password(self, service, username):
        res = self._get_password(service)
        if not res or res['UserName'] != username:
            res = self._get_password(self._compound_name(username, service))
        if not res:
            return
        else:
            blob = res['CredentialBlob']
            return blob.decode('utf-16')

    def _get_password(self, target):
        try:
            res = win32cred.CredRead(Type=(win32cred.CRED_TYPE_GENERIC),
              TargetName=target)
        except pywintypes.error as e:
            e = OldPywinError.wrap(e)
            if e.winerror == 1168:
                if e.funcname == 'CredRead':
                    return
            raise

        return res

    def set_password(self, service, username, password):
        existing_pw = self._get_password(service)
        if existing_pw:
            existing_username = existing_pw['UserName']
            target = self._compound_name(existing_username, service)
            self._set_password(target, existing_username, existing_pw['CredentialBlob'].decode('utf-16'))
        self._set_password(service, username, str(password))

    def _set_password(self, target, username, password):
        credential = dict(Type=(win32cred.CRED_TYPE_GENERIC),
          TargetName=target,
          UserName=username,
          CredentialBlob=password,
          Comment='Stored using python-keyring',
          Persist=(self.persist))
        win32cred.CredWrite(credential, 0)

    def delete_password(self, service, username):
        compound = self._compound_name(username, service)
        deleted = False
        for target in (service, compound):
            existing_pw = self._get_password(target)
            if existing_pw and existing_pw['UserName'] == username:
                deleted = True
                self._delete_password(target)

        if not deleted:
            raise PasswordDeleteError(service)

    def _delete_password(self, target):
        try:
            win32cred.CredDelete(Type=(win32cred.CRED_TYPE_GENERIC), TargetName=target)
        except pywintypes.error as e:
            e = OldPywinError.wrap(e)
            if e.winerror == 1168:
                if e.funcname == 'CredDelete':
                    return
            raise

    def get_credential(self, service, username):
        res = None
        if username:
            res = self._get_password(self._compound_name(username, service))
        if not res:
            res = self._get_password(service)
            return res or None
        else:
            return SimpleCredential(res['UserName'], res['CredentialBlob'].decode('utf-16'))


class OldPywinError:
    __doc__ = '\n    A compatibility wrapper for old PyWin32 errors, such as reported in\n    https://bitbucket.org/kang/python-keyring-lib/issue/140/\n    '

    def __init__(self, orig):
        self.orig = orig

    @property
    def funcname(self):
        return self.orig[1]

    @property
    def winerror(self):
        return self.orig[0]

    @classmethod
    def wrap(cls, orig_err):
        attr_check = functools.partial(hasattr, orig_err)
        is_old = not all(map(attr_check, ['funcname', 'winerror']))
        if is_old:
            return cls(orig_err)
        else:
            return orig_err