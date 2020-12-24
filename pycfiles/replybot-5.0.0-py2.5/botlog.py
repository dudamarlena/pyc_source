# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/botlog.py
# Compiled at: 2008-08-09 12:39:34
"""Set up logging."""
__metaclass__ = type
__all__ = [
 'initialize']
import os, errno, logging
from botlib.configuration import config
FMT = '%(asctime)s (%(process)d) %(message)s'
DATEFMT = '%b %d %H:%M:%S %Y'

def initialize():
    """Initialize the logging subsystem."""
    logging.basicConfig(format=FMT, datefmt=DATEFMT, level=logging.INFO)
    log = logging.getLogger('replybot')
    log.setLevel(config.log_level)
    log.propagate = config.options.debug
    if config.log_file == 'Console':
        handler = logging.StreamHandler()
    else:
        try:
            os.makedirs(os.path.dirname(config.log_file), 1472)
        except OSError, error:
            if error.errno != errno.EEXIST:
                raise

        handler = logging.FileHandler(config.log_file)
    formatter = logging.Formatter(fmt=FMT, datefmt=DATEFMT)
    handler.setFormatter(formatter)
    log.addHandler(handler)