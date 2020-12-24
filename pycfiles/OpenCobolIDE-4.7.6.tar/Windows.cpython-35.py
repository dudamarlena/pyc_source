# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/OpenCobolIDE/open_cobol_ide/extlibs/keyring/backends/Windows.py
# Compiled at: 2016-12-30 07:03:12
# Size of source mod 2**32: 4904 bytes
import functools
from ..py27compat import unicode_str
from ..util import escape, properties
from ..backend import KeyringBackend
from ..errors import PasswordDeleteError, ExceptionRaisedContext
try:
    from win32ctypes import pywintypes
    from win32ctypes import win32cred
    win32cred.__name__
except ImportError:
    try:
        import pywintypes, win32cred
    except ImportError:
        pass

def has_pywin32():
    """
    Does this environment have pywin32?
    Should return False even when Mercurial's Demand Import allowed import of
    win32cred.
    """
    with ExceptionRaisedContext() as (exc):
        win32cred.__name__
    return not bool(exc)


class WinVaultKeyring(KeyringBackend):
    __doc__ = "\n    WinVaultKeyring stores encrypted passwords using the Windows Credential\n    Manager.\n\n    Requires pywin32\n\n    This backend does some gymnastics to simulate multi-user support,\n    which WinVault doesn't support natively. See\n    https://bitbucket.org/kang/python-keyring-lib/issue/47/winvaultkeyring-only-ever-returns-last#comment-731977\n    for details on the implementation, but here's the gist:\n\n    Passwords are stored under the service name unless there is a collision\n    (another password with the same service name but different user name),\n    in which case the previous password is moved into a compound name:\n    {username}@{service}\n    "

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        If available, the preferred backend on Windows.
        """
        if not has_pywin32():
            raise RuntimeError('Requires Windows and pywin32')
        return 5

    @staticmethod
    def _compound_name(username, service):
        return escape.u('%(username)s@%(service)s') % vars()

    def get_password(self, service, username):
        res = self._get_password(service)
        if not res or res['UserName'] != username:
            res = self._get_password(self._compound_name(username, service))
        if not res:
            return
        blob = res['CredentialBlob']
        return blob.decode('utf-16')

    def _get_password(self, target):
        try:
            res = win32cred.CredRead(Type=win32cred.CRED_TYPE_GENERIC, TargetName=target)
        except pywintypes.error as e:
            e = OldPywinError.wrap(e)
            if e.winerror == 1168 and e.funcname == 'CredRead':
                return
            raise

        return res

    def set_password(self, service, username, password):
        existing_pw = self._get_password(service)
        if existing_pw:
            existing_username = existing_pw['UserName']
            target = self._compound_name(existing_username, service)
            self._set_password(target, existing_username, existing_pw['CredentialBlob'].decode('utf-16'))
        self._set_password(service, username, unicode_str(password))

    def _set_password(self, target, username, password):
        credential = dict(Type=win32cred.CRED_TYPE_GENERIC, TargetName=target, UserName=username, CredentialBlob=password, Comment='Stored using python-keyring', Persist=win32cred.CRED_PERSIST_ENTERPRISE)
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
        win32cred.CredDelete(Type=win32cred.CRED_TYPE_GENERIC, TargetName=target)


class OldPywinError(object):
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
        return orig_err