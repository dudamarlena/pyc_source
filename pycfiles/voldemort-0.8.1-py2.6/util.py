# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/voldemort/util.py
# Compiled at: 2013-08-02 16:30:40
import sys, traceback, logging, logging.handlers

def setup_logging(path, level):
    """Setup application logging.
    """
    log_handler = logging.handlers.RotatingFileHandler(path, maxBytes=1048576, backupCount=2)
    root_logger = logging.getLogger('')
    root_logger.setLevel(level)
    format = '%(name)s - %(message)s'
    formatter = logging.Formatter(format)
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('--> %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)


def print_traceback():
    """Get the exception traceback.
    """
    (exc_type, exc_value, exc_traceback) = sys.exc_info()
    return ('').join(traceback.format_exception(exc_type, exc_value, exc_traceback))