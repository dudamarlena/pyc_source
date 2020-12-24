# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/demo/local_settings.py
# Compiled at: 2013-03-24 20:47:55
from tlsauth import CertAuthority
TLS_CA = CertAuthority('/home/stef/tasks/tlsauth/CA/public/root.pem', '/home/stef/tasks/tlsauth/CA/private/root.pem', '/home/stef/tasks/tlsauth/CA/conf/serial', '/home/stef/tasks/tlsauth/CA/dummy.pem', 'http://www.example.com/crl.pem', '/home/stef/tasks/tlsauth/CA/incoming')
TLS_ADMINGROUPS = [
 'CA admins']
TLS_SCRUTINIZER = None
TLS_BLINDSIGN = False