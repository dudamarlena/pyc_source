# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/command_executor.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 362 bytes
import os
from allrank.utils.ltr_logging import get_logger
logger = get_logger()

def execute_command(command):
    logger.info('will execute {}'.format(command))
    result = os.system(command)
    logger.info('exit_code = {}'.format(result))
    if result != 0:
        raise RuntimeError("non-zero exit-code: {} from command '{}'".format(result, command))