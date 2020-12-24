# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/auth/http.py
# Compiled at: 2010-08-08 03:18:44
try:
    from crypt import crypt
except ImportError:
    from fcrypt import crypt

def htpasswd_login(username, password, config):
    authn_file = getattr(config, 'authn_file', '')
    if isinstance(username, str):
        username = unicode(username, 'utf-8')
    if authn_file:
        pwdfile = open(authn_file)
        for line in pwdfile:
            if line.strip().startswith('#') and ':' not in line:
                continue
            (user, pwdhash) = line.strip().split(':', 1)
            if username == unicode(user, 'utf-8'):
                if pwdhash == crypt(password, pwdhash[:2]):
                    return True
                break

    return False