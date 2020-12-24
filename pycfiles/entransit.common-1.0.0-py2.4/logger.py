# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\entransit\common\logger.py
# Compiled at: 2008-03-07 16:10:41
"""
$Id: __init__.py 732 2005-01-21 19:43:40Z sidnei $
"""
import os, sys, logging
from logging import WARNING, INFO, DEBUG
BLATHER = 15
TRACE = 5
logging._levelNames['TRACE'] = TRACE
logging._levelNames['BLATHER'] = BLATHER
_pid = str(os.getpid())
logger = None

def _setupLogging(level=TRACE):
    global logger
    logger = logging.getLogger('entransit')
    logger.setLevel(level)
    fmt = logging.Formatter('------\n%(asctime)s %(levelname)s %(name)s %(message)s', '%Y-%m-%dT%H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    zeolog = logging.getLogger('ZEO.zrpc')
    zeolog.setLevel(level)
    zeolog.addHandler(handler)


def setupLogging():
    """Initialize the logging module.
    """
    global logger
    import logging.config
    logini = (
     os.path.join(os.getenv('INSTANCE_HOME', ''), 'etc', 'log.ini'), os.path.abspath('log.ini'), os.path.join(sys.prefix, 'entransit', 'config', 'log.ini'))
    found = False
    for fname in logini:
        if os.path.exists(fname):
            found = True
            logging.config.fileConfig(fname)
            break

    if not found:
        logging.basicConfig()
        level = TRACE
        if os.environ.has_key('LOGGING'):
            level = int(os.environ['LOGGING'])
        _setupLogging(level)
    if os.environ.has_key('LOGGING'):
        level = int(os.environ['LOGGING'])
        logging.getLogger().setLevel(level)
    logger = logging.getLogger('entransit')


def log(msg, level=INFO, exc_info=False):
    """Internal: generic logging function.
    """
    if logger is None:
        return
    message = '(%s) %s' % (_pid, msg)
    logger.log(level, message, exc_info=exc_info)
    return