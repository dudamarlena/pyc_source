# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/examples/authenticate.py
# Compiled at: 2013-08-11 10:36:51
from pyws.errors import AccessDenied
soap_headers_schema = {0: 'Headers', 
   'username': str, 
   'password': str}

def authenticate(data):
    if data != {'username': 'user', 'password': 'pass'}:
        raise AccessDenied(data and data.get('username'))
    return data.get('username')