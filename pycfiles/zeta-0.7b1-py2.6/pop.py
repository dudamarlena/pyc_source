# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/pop.py
# Compiled at: 2010-06-17 10:01:45
"""POP Client to receive mails.
Mails are sent for,
    * Inviting users
    * Sending urls for resetting forgotten password
    * Notifications on timeline logs

config parameters used,
    zeta.smtp_serverip,
    zeta.smtp_user,
    zeta.smtp_password,
from .ini file to login into SMTP server.
"""
serverip = None
login = None
password = None

def _fetchconfig():
    """Same smtp configurations are used for pop3 as well"""
    global login
    global password
    global serverip
    if serverip == None:
        serverip = h.fromconfig('zeta.smtp_serverip')
        login = h.fromconfig('zeta.smtp_user')
        password = h.fromconfig('zeta.smtp_password')
    return (
     serverip, login, password)