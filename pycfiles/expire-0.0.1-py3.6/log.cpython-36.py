# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/expire/log.py
# Compiled at: 2018-03-05 19:51:17
# Size of source mod 2**32: 858 bytes
import logging, colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

class Logger:
    __doc__ = '\n    Token from https://github.com/gaojiuli/toapi/blob/master/toapi/log.py\n    '

    def __init__(self, name, level=logging.DEBUG):
        logging.basicConfig(format='%(asctime)s %(message)-10s ', datefmt='%Y/%m/%d %H:%M:%S')
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def info(self, color, type, message):
        self.logger.info(color + '[%-8s] %-2s %s' % (type, 'OK', message) + Style.RESET_ALL)

    def error(self, type, message):
        self.logger.error(Fore.RED + '[%-8s] %-4s %s' % (type, 'FAIL', message) + Style.RESET_ALL)

    def exception(self, type, message):
        self.error(type, message)


logger = Logger(__name__)