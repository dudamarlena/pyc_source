# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/auth/ldap_login.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.model.ldap_api import LDAP

def ldap_login(username, password, config):
    """ get authentication data from form, authenticate against LDAP (or Active
        Directory), fetch some user infos from LDAP and create a user object
        for that user. The session is kept by the moin_session auth plugin.
    """
    if not password or not username or not config:
        return False
    return LDAP(config).test_login(username, password)