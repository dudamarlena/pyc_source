# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/log/logger.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 4062 bytes
"""
module dealing with log in color

https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
"""
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '22/09/2017'
import logging
from tomwer.core.log.processlog import PROCESS_ENDED_NAME, PROCESS_SKIPPED_NAME, PROCESS_INFORM_LEVEL
import os
_RESET_SEQ = '\x1b[0m'
_COLOR_SEQ = '\x1b[1;%dm'
_BOLD_SEQ = '\x1b[1m'
_BLACK, _RED, _GREEN, _YELLOW, _BLUE, _MAGENTA, _CYAN, _WHITE = range(8)
LOG_COLORS = {'WARNING': _YELLOW, 
 'INFO': _BLACK, 
 'DEBUG': _BLUE, 
 'CRITICAL': _YELLOW, 
 'ERROR': _RED, 
 PROCESS_SKIPPED_NAME: _MAGENTA, 
 PROCESS_ENDED_NAME: _GREEN, 
 PROCESS_INFORM_LEVEL: _BLACK}

def _formatter_message(message, use_color=True):
    if use_color is True:
        message = message.replace('$RESET', _RESET_SEQ).replace('$BOLD', _BOLD_SEQ)
    else:
        message = message.replace('$RESET', '').replace('$BOLD', '')
    return message


class _ColoredFormatter(logging.Formatter):

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)
        self.use_color = os.environ.get('ORANGE_COLOR_STDOUT_LOG', 'False') == 'True'

    def format(self, record):
        levelname = record.levelname
        if self.use_color is True:
            if levelname in LOG_COLORS:
                levelname_color = _COLOR_SEQ % (30 + LOG_COLORS[levelname]) + levelname + _RESET_SEQ
                record.levelname = levelname_color
        record.asctime = self.formatTime(record, self.datefmt)
        return logging.Formatter.format(self, record)


class TomwerLogger(logging.Logger):
    __doc__ = '\n    Custom logger class with multiple destinations\n    '
    FORMAT = '%(asctime)s [%(levelname)-18s] %(message)s [$BOLD%(name)-20s$RESET]($BOLD%(filename)s$RESET:%(lineno)d)'

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)
        self.name = name
        self.color_format = _formatter_message((TomwerLogger.FORMAT), use_color=(os.environ.get('ORANGE_COLOR_STDOUT_LOG', 'False') == 'True'))
        color_formatter = _ColoredFormatter(self.color_format)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)

    def __str__(self):
        return self.name


logging.setLoggerClass(TomwerLogger)
if __name__ == '__main__':
    logger = TomwerLogger(logging.getLogger('test logger'))
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')