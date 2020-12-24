# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/sleep.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from time import sleep as callback_function
from doorpi.action.base import SingleAction

def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) is not 1:
        return None
    else:
        time = float(parameter_list[0])
        return SleepAction(callback_function, time)


class SleepAction(SingleAction):
    pass