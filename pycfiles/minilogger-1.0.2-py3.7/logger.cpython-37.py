# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minilogger/logger.py
# Compiled at: 2019-05-04 11:58:31
# Size of source mod 2**32: 1507 bytes
from os import get_terminal_size as termSize

class logger:
    HEADER = '\x1b[95m'
    INFO = '\x1b[94m'
    SUCCESS = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    NORMAL = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    RESET = '\x1b[0m'
    FLAG_SHORT_LOGS = False
    MAX_LEN_LOGS = termSize().columns - 1

    @staticmethod
    def log(str, color=RESET, endChr='\n'):
        if logger.FLAG_SHORT_LOGS:
            str = logger._shortenString(str)
        print((color + str + logger.RESET), end=endChr)

    @staticmethod
    def _shortenString(str):
        if len(str) <= logger.MAX_LEN_LOGS:
            return str
        halfLine = int(logger.MAX_LEN_LOGS / 2)
        return str[:halfLine - 2] + '...' + str[-halfLine + 1:]


if __name__ == '__main__':
    logger.log('This is a test', logger.BOLD + logger.SUCCESS)
    for i in range(1, 100):
        logger.log('{}/{} files processed...'.format(i, 100), logger.INFO, '\r')

    logger.FLAG_SHORT_LOGS = True
    logger.MAX_LEN_LOGS = 40