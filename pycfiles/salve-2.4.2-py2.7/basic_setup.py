# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/log/basic_setup.py
# Compiled at: 2015-11-06 23:45:35
import logging
from .handler import gen_handler

def clear_handlers(logger):
    """
    Clear logger handlers.
    """
    logger.handlers = []


def add_logfile(logger, loglevel, filename):
    """
    Adds a handler which writes to a file to the logger's handlers.
    """
    hdlr = gen_handler(filename=filename)
    hdlr.setLevel(loglevel)
    logger.addHandler(hdlr)


def create_logger(name):
    l = logging.getLogger(name)
    setup_stderr(l)
    l.propagate = False
    return l


def setup_stderr(logger):
    """
    Does the bare minimum to setup a working log handler which writes to
    stderr.

    Args:
        @logger
        A logging.Logger object.
    """
    hdlr = gen_handler()
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)


def str_to_level(lvlstr):
    try:
        return dict((logging.getLevelName(l), l) for l in [
         logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
         logging.CRITICAL])[lvlstr.upper()]
    except KeyError:
        raise ValueError(('{0} is not a valid log level').format(lvlstr))