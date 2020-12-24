# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pwauth/store.py
# Compiled at: 2007-05-27 23:50:52
try:
    import subprocess
except ImportError:
    import _subprocess as subprocess

from trac.core import *
from trac.config import Option
from acct_mgr.api import IPasswordStore

class PwAuthStore(Component):
    """A password backend for AccountManager that uses pwauth."""
    implements(IPasswordStore)
    pwauth_path = Option('pwauth', 'path', default='/usr/sbin/pwauth', doc='Path to the pwauth program')

    def check_password(self, user, password):
        proc = subprocess.Popen([self.pwauth_path], stdin=subprocess.PIPE)
        proc.communicate('%s\n%s\n' % (user, password))
        return proc.returncode == 0