# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/logger.py
# Compiled at: 2017-10-30 03:09:30
# Size of source mod 2**32: 3080 bytes
"""
Logging functions.

At the beginning of the ODCS flow, init_logging(conf) must be called.

After that, logging from any module is possible using Python's "logging"
module as showed at
<https://docs.python.org/3/howto/logging.html#logging-basic-tutorial>.

Examples:

import logging

logging.debug("Phasers are set to stun.")
logging.info("%s tried to build something", username)
logging.warn("%s failed to build", task_id)

"""
import logging
levels = {}
levels['debug'] = logging.DEBUG
levels['error'] = logging.ERROR
levels['warning'] = logging.WARNING
levels['info'] = logging.INFO

def str_to_log_level(level):
    """
    Returns internal representation of logging level defined
    by the string `level`.

    Available levels are: debug, info, warning, error
    """
    if level not in levels:
        return logging.NOTSET
    else:
        return levels[level]


def supported_log_backends():
    return ('console', 'journal', 'file')


def init_logging(conf):
    """
    Initializes logging according to configuration file.
    """
    log_format = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    log_backend = conf.log_backend
    if not log_backend or len(log_backend) == 0 or log_backend == 'console':
        logging.basicConfig(level=(conf.log_level), format=log_format)
        log = logging.getLogger()
        log.setLevel(conf.log_level)
    else:
        if log_backend == 'journal':
            logging.basicConfig(level=(conf.log_level), format=log_format)
            try:
                from systemd import journal
            except Exception:
                raise ValueError('systemd.journal module is not installed')

            log = logging.getLogger()
            log.propagate = False
            log.addHandler(journal.JournalHandler())
        else:
            logging.basicConfig(filename=(conf.log_file), level=(conf.log_level), format=log_format)
            log = logging.getLogger()