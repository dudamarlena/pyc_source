# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/SingleActions/os_execute.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import subprocess
from doorpi.action.base import SingleAction
import doorpi

def fire_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()


def get(parameters):
    parsed_parameters = doorpi.DoorPi().parse_string(parameters)
    return OsExecuteAction(fire_command, command=parsed_parameters)


class OsExecuteAction(SingleAction):
    pass