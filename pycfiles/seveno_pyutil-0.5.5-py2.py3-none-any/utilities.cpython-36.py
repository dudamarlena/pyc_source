# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/logging_utilities/utilities.py
# Compiled at: 2019-03-13 06:22:26
# Size of source mod 2**32: 1237 bytes
import logging, sys, traceback
from logging import NullHandler

def silence_logger(logger):
    """
    For given logger, replaces all its handlers with
    :class:`logging.NullHandler`.
    """
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])

    logger.addHandler(NullHandler())


def log_to_console_for(logger_name):
    """
    Sometimes, usually during development, we want to quickly see output of
    some particular package logger. This method will configure such logger
    to spit stuff out to console.
    """
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def log_to_tmp_file_for(logger_name, file_path='/tmp/seveno_pyutil.log'):
    """
    Quick setup for given logger directing it to ``/tmp/seveno_pyutil.log``
    This is of course mainly used during development, especially when playing
    with things in Python console.
    """
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(filename=file_path)
    handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)