# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/drivers/MySQL/Config.py
# Compiled at: 2016-03-23 14:50:18
from voluptuous import Optional, Required

class Config(object):
    SCHEMA = {Required('user'): str, 
       Required('password'): str, 
       Required('database'): str, 
       Optional('host'): str, 
       Optional('use_ssl'): bool, 
       Optional('timeout'): str, 
       Optional('ssl_ca'): str, 
       Optional('ssl_cert'): str, 
       Optional('ssl_key'): str, 
       Optional('compress'): bool, 
       Optional('port'): int}