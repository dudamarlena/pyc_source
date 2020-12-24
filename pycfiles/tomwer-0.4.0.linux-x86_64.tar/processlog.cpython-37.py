# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/processlog.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2134 bytes
"""
Simple logs levels definition relative to process status
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/09/2017'
import logging
PROCESS_ENDED_LEVEL = 35
PROCESS_SKIPPED_LEVEL = 36
logging.addLevelName(PROCESS_ENDED_LEVEL, 'PROCESS_ENDED')
logging.addLevelName(PROCESS_SKIPPED_LEVEL, 'PROCESS_SKIPPED')

def processEnded(self, message, *args, **kws):
    if self.isEnabledFor(PROCESS_ENDED_LEVEL):
        (self._log)(PROCESS_ENDED_LEVEL, message, args, **kws)


def processSkipped(self, message, *args, **kws):
    if self.isEnabledFor(PROCESS_SKIPPED_LEVEL):
        (self._log)(PROCESS_SKIPPED_LEVEL, message, args, **kws)


logging.Logger.processEnded = processEnded
logging.Logger.processSkipped = processSkipped