# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/hangup.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import doorpi
from doorpi.action.base import SingleAction
from time import sleep

def hangup(waittime):
    logger.trace('hangup requested')
    if waittime > 0:
        logger.debug('Waiting %s seconds before sending hangup request', waittime)
        sleep(float(waittime))
    return doorpi.DoorPi().sipphone.hangup()


def get(parameters):
    if not parameters.isdigit():
        return None
    else:
        return HangupAction(hangup, parameters)


class HangupAction(SingleAction):
    pass