# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/sipphone/SipphoneInterface.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import importlib, doorpi

class SipphoneNotExists(Exception):
    pass


def load_sipphone():
    conf_pre = ''
    conf_post = ''
    sipphone_name = doorpi.DoorPi().config.get('SIP-Phone', 'sipphonetyp', find_first_installed_sipphone())
    try:
        sipphone = importlib.import_module('doorpi.sipphone.from_' + sipphone_name).get(sipphone_name=sipphone_name, conf_pre=conf_pre, conf_post=conf_post)
    except ImportError as exp:
        logger.exception('sipphone %s not found @ sipphone.from_%s with exception %s', sipphone_name, sipphone_name, exp)
        logger.warning('use dummy sipphone after last exception!')
        sipphone = importlib.import_module('doorpi.sipphone.from_dummy').get(sipphone_name=sipphone_name, conf_pre=conf_pre, conf_post=conf_post)

    return sipphone


def find_first_installed_sipphone():
    sipphone_status = doorpi.DoorPi().get_status(['environment'], ['sipphone'])
    sipphones = sipphone_status.dictionary['environment']['sipphone']['libraries']
    for sipphone_name in sipphones.keys():
        if sipphones[sipphone_name]['status']['installed']:
            logger.info('found installed sipphone "%s" and use this as default', sipphone_name)
            return sipphone_name

    logger.warning('found no installed sipphones and use dummy as default')
    return 'dummy'