# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/webserver_lib/request_handler_static_functions.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import doorpi

def control_config_get_value(section, key, default='', store='True'):
    return doorpi.DoorPi().config.get_string(section=section, key=key, default=default, store_if_not_exists=True if store.lower() == 'true' else False)


def control_config_set_value(section, key, value, password='False'):
    return doorpi.DoorPi().config.set_value(section=section, key=key, value=value, password=True if password.lower() == 'true' else False)


def control_config_delete_key(section, key):
    return doorpi.DoorPi().config.delete_key(section=section, key=key)


def control_config_save(configfile=''):
    return doorpi.DoorPi().config.save_config(configfile=configfile)


def control_config_get_configfile():
    return doorpi.DoorPi().config.config_file or ''