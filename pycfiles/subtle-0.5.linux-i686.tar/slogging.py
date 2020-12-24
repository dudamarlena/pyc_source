# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/slogging.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
import logging, sys, os, os.path
GREEN_FONT = b'\x1b[0;32m'
YELLOW_FONT = b'\x1b[0;33m'
BLUE_FONT = b'\x1b[0;34m'
RED_FONT = b'\x1b[0;31m'
RESET_FONT = b'\x1b[0m'

def setupLogging(colored=True, with_time=False, with_thread=False, filename=None):
    """Set up a nice colored logger as the main application logger."""

    class SimpleFormatter(logging.Formatter):

        def __init__(self, with_time, with_thread):
            self.fmt = (b'%(asctime)s ' if with_time else b'') + b'%(levelname)-8s ' + b'[%(name)s:%(funcName)s]' + (b'[%(threadName)s]' if with_thread else b'') + b' -- %(message)s'
            logging.Formatter.__init__(self, self.fmt)

    class ColoredFormatter(logging.Formatter):

        def __init__(self, with_time, with_thread):
            self.fmt = (b'%(asctime)s ' if with_time else b'') + b'-CC-%(levelname)-8s ' + BLUE_FONT + b'[%(name)s:%(funcName)s]' + RESET_FONT + (b'[%(threadName)s]' if with_thread else b'') + b' -- %(message)s'
            logging.Formatter.__init__(self, self.fmt)

        def format(self, record):
            modpath = record.name.split(b'.')
            record.mname = modpath[0]
            record.mmodule = (b'.').join(modpath[1:])
            result = logging.Formatter.format(self, record)
            if record.levelno == logging.DEBUG:
                color = BLUE_FONT
            elif record.levelno == logging.INFO:
                color = GREEN_FONT
            elif record.levelno == logging.WARNING:
                color = YELLOW_FONT
            else:
                color = RED_FONT
            result = result.replace(b'-CC-', color)
            return result

    if filename is not None:
        logdir = os.path.dirname(filename)
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        ch = logging.FileHandler(filename, mode=b'w')
        ch.setFormatter(SimpleFormatter(with_time, with_thread))
    else:
        ch = logging.StreamHandler()
        if colored and sys.platform != b'win32':
            ch.setFormatter(ColoredFormatter(with_time, with_thread))
        else:
            ch.setFormatter(SimpleFormatter(with_time, with_thread))
    logging.getLogger().addHandler(ch)
    return