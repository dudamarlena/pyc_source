# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/logger.py
# Compiled at: 2012-08-27 04:35:26
import logging, logging.config
from secobj.localization import _
LOG = None
LOG_BASE = None

def getlogger(*args):
    global LOG
    global LOG_BASE
    if LOG is None:
        raise ValueError, _('Logger is not initialized')
    if len(args) > 0:
        names = [
         LOG_BASE]
        names.extend(args)
        return logging.getLogger(('.').join(names))
    else:
        return LOG


def initlogger(base, configfile=None):
    global LOG
    global LOG_BASE
    if LOG is None:
        if not isinstance(base, basestring):
            raise ValueError, _('Invalid logger base, must be a string')
        if configfile is not None:
            logging.config.fileConfig(configfile)
        LOG_BASE = base
        LOG = logging.getLogger(LOG_BASE)
        if len(LOG.handlers) == 0:
            LOG.addHandler(logging.NullHandler())
    return