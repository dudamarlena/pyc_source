# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/conf/backward_compatibility.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
BACKWARD_COMPATIBILITY_KEYS = {'SIP-Phone': {'sipserver_server': ('SIP-Phone', 'server'), 
                 'sipserver_username': ('SIP-Phone', 'username'), 
                 'sipserver_password': ('SIP-Phone', 'password'), 
                 'sipserver_realm': ('SIP-Phone', 'realm'), 
                 'dialtone': ('DoorPi', 'dialtone'), 
                 'dialtone_renew_every_start': ('DoorPi', 'dialtone_renew_every_start'), 
                 'dialtone_volume': ('DoorPi', 'dialtone_volume'), 
                 'records': ('DoorPi', 'records'), 
                 'record_while_dialing': ('DoorPi', 'record_while_dialing')}}

def convert_config_to_json(config_object):
    return config_object