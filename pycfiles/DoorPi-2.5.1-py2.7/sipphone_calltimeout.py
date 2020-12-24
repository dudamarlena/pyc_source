# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/sipphone_calltimeout.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi
from time import sleep

def sipphone_calltimeout(timeout, *callstate_to_check):
    try:
        doorpi.DoorPi().sipphone.lib.thread_register('pjsip_handle_events')
        return doorpi.DoorPi().sipphone.call_timeout(timeout, callstate_to_check)
    except:
        return False


def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) < 1:
        return None
    else:
        timeout = int(parameter_list[0])
        callstate_to_check = parameter_list[1:]
        return SipphoneCallTimeoutAction(sipphone_calltimeout, timeout=timeout)


class SipphoneCallTimeoutAction(SingleAction):
    pass