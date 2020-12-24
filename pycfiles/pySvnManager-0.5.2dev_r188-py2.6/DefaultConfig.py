# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/config/DefaultConfig.py
# Compiled at: 2010-08-08 03:18:43
from pylons import config

class DefaultConfig:
    """ Default config values 
    Warning: do not change configuration here, change localconfig.py instead.
    Save localconfig.py.ini to the deploy directory as localconfig.py.
    """
    if config.get('__file__') is None:
        import pylons.test
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
    authn_file = config.get('authn_file', '') % {'here': config.get('here')}
    authz_file = config.get('authz_file', '') % {'here': config.get('here')}
    log_per_page = 10
    repos_root = config.get('repos_root', '') % {'here': config.get('here')}
    ldap_base = None
    ldap_uri = 'ldap://localhost'
    ldap_binddn = ''
    ldap_bindpw = ''
    ldap_scope = 2
    ldap_filter = '(&(uid=%(username)s)(authorizedService=svn)(ossxpConfirmed=TRUE))'
    ldap_timeout = 10
    ldap_coding = 'utf-8'
    ldap_start_tls = False
    ldap_uid_attribute = 'uid'
    ldap_aliasname_attribute = 'cn'
    ldap_surname_attribute = 'sn'
    ldap_givenname_attribute = 'givenName'
    ldap_email_attribute = 'mail'