# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/call.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi

def call(number):
    doorpi.DoorPi().sipphone.call(number)


def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) is not 1:
        return None
    else:
        number = parameter_list[0]
        return CallAction(call, number=number)


class CallAction(SingleAction):
    pass