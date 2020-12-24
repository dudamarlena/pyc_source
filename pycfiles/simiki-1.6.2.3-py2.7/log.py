# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/log.py
# Compiled at: 2017-06-02 11:17:28
from __future__ import absolute_import, unicode_literals
import logging
from logging import getLogger, Formatter, StreamHandler
from simiki import utils
from simiki.compat import is_linux, is_osx

class ANSIFormatter(Formatter):
    """Use ANSI escape sequences to colored log"""

    def format(self, record):
        try:
            msg = super(ANSIFormatter, self).format(record)
        except:
            msg = Formatter.format(self, record)

        lvl2color = {b'DEBUG': b'blue', 
           b'INFO': b'green', 
           b'WARNING': b'yellow', 
           b'ERROR': b'red', 
           b'CRITICAL': b'bgred'}
        rln = record.levelname
        if rln in lvl2color:
            return (b'[{0}]: {1}').format(utils.color_msg(lvl2color[rln], rln), msg)
        else:
            return msg


class NonANSIFormatter(Formatter):
    """Non ANSI color format"""

    def format(self, record):
        try:
            msg = super(NonANSIFormatter, self).format(record)
        except:
            msg = Formatter.format(self, record)

        rln = record.levelname
        return (b'[{0}]: {1}').format(rln, msg)


def _is_platform_allowed_ansi():
    """ansi be used on linux/macos"""
    if is_linux or is_osx:
        return True
    return False


def logging_init(level=None, logger=getLogger(), handler=StreamHandler(), use_color=True):
    if use_color and _is_platform_allowed_ansi():
        fmt = ANSIFormatter()
    else:
        fmt = NonANSIFormatter()
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    if level:
        logger.setLevel(level)


if __name__ == b'__main__':
    logging_init(level=logging.DEBUG)
    root_logger = logging.getLogger()
    root_logger.debug(b'debug')
    root_logger.info(b'info')
    root_logger.warning(b'warning')
    root_logger.error(b'error')
    root_logger.critical(b'critical')