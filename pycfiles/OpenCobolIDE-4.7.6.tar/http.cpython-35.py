# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/http.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1255 bytes
"""
urllib2.HTTPPasswordMgr object using the keyring, for use with the
urllib2.HTTPBasicAuthHandler.

usage:
    import urllib2
    handlers = [urllib2.HTTPBasicAuthHandler(PasswordMgr())]
    urllib2.install_opener(handlers)
    urllib2.urlopen(...)

This will prompt for a password if one is required and isn't already
in the keyring. Then, it adds it to the keyring for subsequent use.
"""
import getpass
from . import get_password, delete_password, set_password

class PasswordMgr(object):

    def get_username(self, realm, authuri):
        return getpass.getuser()

    def add_password(self, realm, authuri, password):
        user = self.get_username(realm, authuri)
        set_password(realm, user, password)

    def find_user_password(self, realm, authuri):
        user = self.get_username(realm, authuri)
        password = get_password(realm, user)
        if password is None:
            prompt = 'password for %(user)s@%(realm)s for %(authuri)s: ' % vars()
            password = getpass.getpass(prompt)
            set_password(realm, user, password)
        return (
         user, password)

    def clear_password(self, realm, authuri):
        user = self.get_username(realm, authuri)
        delete_password(realm, user)