# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alec/projects/toltech.cn/khan/khan/deploy/logging.py
# Compiled at: 2010-07-22 00:46:43
from __future__ import absolute_import
import logging, platform
__all__ = [
 'ColorFormatter']

class _ColorFormatter(logging.Formatter):
    """
    多彩日志实现, 不支持 Windows
    """
    FORMAT = '[%(asctime)s][$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)'
    (BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE) = range(8)
    RESET_SEQ = '\x1b[0m'
    COLOR_SEQ = '\x1b[1;%dm'
    BOLD_SEQ = '\x1b[1m'
    COLORS = {'WARNING': YELLOW, 
       'INFO': WHITE, 
       'DEBUG': BLUE, 
       'CRITICAL': YELLOW, 
       'ERROR': RED}

    def formatter_msg(self, msg, use_color=True):
        if use_color:
            msg = msg.replace('$RESET', self.RESET_SEQ).replace('$BOLD', self.BOLD_SEQ)
        else:
            msg = msg.replace('$RESET', '').replace('$BOLD', '')
        return msg

    def __init__(self, fmt=None, datefmt=None):
        msg = self.formatter_msg(fmt or self.FORMAT, True)
        logging.Formatter.__init__(self, msg)
        if platform.system() != 'Windows':
            self.use_color = True
        else:
            self.use_color = False

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            fore_color = 30 + self.COLORS[levelname]
            levelname_color = self.COLOR_SEQ % fore_color + levelname + self.RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


if platform.system().upper() not in ('WINDOWS', ):
    ColorFormatter = _ColorFormatter
else:
    ColorFormatter = logging.Formatter