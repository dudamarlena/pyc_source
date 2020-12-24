# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/MetaStalk/utils/logger.py
# Compiled at: 2020-05-08 18:09:31
# Size of source mod 2**32: 855 bytes
"""Makes the logger for the program"""
import logging

def make_logger(name: str, log_level: int) -> logging.Logger:
    """make_logger

    Creates the logger.

    Might look to make this happen in the main script

    Arguments:
        name {str} -- name of the logger
        log_level {int} -- Verbosity of the logger

    Returns:
        logging.Logger -- The logger that gets used.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler(('{}.log'.format(name)), mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger