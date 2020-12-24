# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngsphy/loggingformatter.py
# Compiled at: 2017-10-03 14:46:21
import logging, platform
LOG_LEVEL_CHOICES = [
 'DEBUG', 'INFO', 'WARNING', 'ERROR']

class MEOutputFormatter:
    """
    This module incorporates different constant color values from bash shell
    for a "pretty" visualization of the log.
    """
    PURPLE = '\x1b[95m'
    CYAN = '\x1b[96m'
    DARKCYAN = '\x1b[36m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    END = '\x1b[0m'


class MELoggingFormatter(logging.Formatter):
    """
    This module has been done to modify the way in which the log is written to
    the standard output and the log file.
    """
    FORMATS = {}
    if platform.system() == 'Darwin':
        FORMATS = {'CONFIG': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.BLUE, MEOutputFormatter.END), 
           'ERROR': ('%(asctime)s - {0}{1}%(levelname)s (%(module)s){2}{0}:\t%(message)s{2}').format(MEOutputFormatter.BOLD, MEOutputFormatter.RED, MEOutputFormatter.END), 
           'WARNING': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.YELLOW, MEOutputFormatter.END), 
           'INFO': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.GREEN, MEOutputFormatter.END), 
           'DEBUG': ('%(asctime)s - {0}{1}%(levelname)s{2} (%(module)s:%(lineno)d):\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.PURPLE, MEOutputFormatter.END), 
           'DEFAULT': ('%(asctime)s - {0}%(levelname)s{1}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.END)}
    else:
        FORMATS = {'CONFIG': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.BLUE, MEOutputFormatter.END), 
           'ERROR': ('%(asctime)s - {0}{1}%(levelname)s (%(module)s){2}{0}:\t%(message)s{2}').format(MEOutputFormatter.BOLD, MEOutputFormatter.RED, MEOutputFormatter.END), 
           'WARNING': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.YELLOW, MEOutputFormatter.END), 
           'INFO': ('%(asctime)s - {0}{1}%(levelname)s{2}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.GREEN, MEOutputFormatter.END), 
           'DEBUG': ('%(asctime)s - {0}{1}%(levelname)s{2} (%(module)s|%(funcName)s:%(lineno)d):\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.PURPLE, MEOutputFormatter.END), 
           'DEFAULT': ('%(asctime)s - {0}%(levelname)s{1}:\t%(message)s').format(MEOutputFormatter.BOLD, MEOutputFormatter.END)}

    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        original_fmt = self._fmt
        try:
            self._fmt = MELoggingFormatter.FORMATS[record.levelname]
        except:
            self._fmt = MELoggingFormatter.FORMATS['DEFAULT']

        return logging.Formatter.format(self, record)