# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/utils/_logging.py
# Compiled at: 2020-03-31 14:41:06
# Size of source mod 2**32: 1617 bytes
import logging
DEFAULT_LOG_FMT = '%(asctime)s %(name)-20s %(levelname)-3s : %(message)s'

def setup_logging(verbosity='info', filename=None, log_fmt=DEFAULT_LOG_FMT) -> None:
    """
    Create a basic configuration for the logging library. Set up console and file handler using provided `log_fmt`.
    :param verbosity: verbosity to use, info by default
    :param filename: where to store the log file
    :param log_fmt: format string for logging
    :return: None
    """
    level = parse_logging_level(verbosity)
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(log_fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def parse_logging_level(verbosity: str) -> int:
    """Parse logging verbosity level
    :param verbosity: string representing verbosity, recoginzed strings are {debug, info, warning, error, critical}
    :return: verbosity level as integer
    """
    vu = verbosity.lower()
    if vu == 'debug':
        return logging.DEBUG
    if vu == 'info':
        return logging.INFO
    if vu == 'warning':
        return logging.WARNING
    if vu == 'error':
        return logging.ERROR
    else:
        if vu == 'critical':
            return logging.CRITICAL
        print('Unknown logging level {}'.format(verbosity))
        return logging.INFO