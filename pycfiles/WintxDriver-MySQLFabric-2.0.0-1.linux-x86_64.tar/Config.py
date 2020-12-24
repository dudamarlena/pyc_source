# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/drivers/MySQLFabric/Config.py
# Compiled at: 2016-03-23 14:50:18
from voluptuous import Optional, Required

class Config(object):
    SCHEMA = {Required('host'): str, 
       Required('fabric_user'): str, 
       Required('fabric_password'): str, 
       Required('user'): str, 
       Required('password'): str, 
       Required('global_group'): str, 
       Required('shard_groups'): list, 
       Optional('port'): int, 
       Optional('database_name'): str, 
       Optional('timeout'): int, 
       Optional('poolsize'): int, 
       Optional('bulkquantity'): int, 
       Optional('attempts'): int}