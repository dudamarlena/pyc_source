# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/statuswatchdog.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from doorpi.action.base import SingleAction
import doorpi

def write_status_watchdog(watchdog_path, timeout):
    timeout = int(timeout)
    try:
        watchdog = open(watchdog_path, 'w+')
    except:
        logger.warning('while action write_status_watchdog - error opening watchdog file')
        return False

    try:
        watchdog.write('\n')
        watchdog.flush()
    finally:
        watchdog.close()

    return True


def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) is not 1 and len(parameter_list) is not 2:
        return None
    else:
        watchdog = parameter_list[0]
        timeout = 5
        if len(parameter_list) is 2:
            timeout = int(parameter_list[1])
        return SleepAction(write_status_watchdog, watchdog, timeout)


class SleepAction(SingleAction):
    pass