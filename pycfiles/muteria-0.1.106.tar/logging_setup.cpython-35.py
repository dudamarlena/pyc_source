# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/controller/logging_setup.py
# Compiled at: 2019-09-19 05:11:43
# Size of source mod 2**32: 2223 bytes
""" This module contains functions to setup the logging facility.
    The logging facility make use of the standard logging lib.

    - The function `console_tmp_log_setup` set the format of the log
        to stdout to display logs before the directory containing the 
        project's log files is created. 
        (allow to pretty print status or error on stdout)
    - The function `setup` sets up the log facility to log into files.
        The function must be called only Once
"""
from __future__ import print_function
import logging, logging.handlers
_SETUP_DONE = False

def is_setup():
    global _SETUP_DONE
    return _SETUP_DONE


def setup(logfile=None, logconsole=False, file_level=logging.INFO, console_level=logging.INFO, file_max_bytes=20000, n_file_backups=1, root_name=''):
    global _SETUP_DONE
    if _SETUP_DONE:
        return
    logger = logging.getLogger(root_name)
    logger.setLevel(min(file_level, console_level))
    formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    if logfile is not None:
        fh = logging.handlers.RotatingFileHandler(logfile, mode='a', maxBytes=file_max_bytes, backupCount=n_file_backups)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if logconsole:
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    _SETUP_DONE = True


def console_tmp_log_setup(loglevel=logging.INFO, root_name=''):
    logging.basicConfig(level=loglevel, format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')