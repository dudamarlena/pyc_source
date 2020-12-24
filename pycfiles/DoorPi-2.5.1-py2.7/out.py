# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/out.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi
from doorpi.action.SingleActions.out_triggered import get as fallback_out_triggered

def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) > 3:
        return fallback_out_triggered(parameters)
    pin = parameter_list[0]
    value = parameter_list[1]
    if len(parameter_list) is 2:
        log_output = True
    else:
        log_output = parameter_list[2]
    return OutAction(doorpi.DoorPi().keyboard.set_output, pin=pin, value=value, log_output=log_output)


class OutAction(SingleAction):
    pass