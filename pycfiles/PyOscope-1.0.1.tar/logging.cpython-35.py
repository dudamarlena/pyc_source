# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyosci/logging.py
# Compiled at: 2017-01-12 03:23:10
# Size of source mod 2**32: 1912 bytes
__doc__ = '\nPrepare logging functionality for the module\n'
import sys, logging, os
LOGFORMAT = '[%(asctime)s] %(levelname)s: %(module)s(%(lineno)d):   %(message)s'

def get_logger(loglevel, logfile=None):
    """
    A root logger with a formatted output logging to stdout and a file

    Args:
        loglevel (int): 10,20,30,... the higher the less logging
        logfile (str): write logging to this file as well as stdout
    Returns:
        logging.logger
    """

    def exception_handler(exctype, value, tb):
        logger.critical('Uncaught exception', exc_info=(exctype, value, tb))

    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    ch = None
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            ch = h
            break

    if ch is None:
        ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter(LOGFORMAT)
    ch.setFormatter(formatter)
    if logfile is not None:
        today = datetime.now()
        today = today.strftime('%Y-%m-%d_%H-%M')
        logend = '.log'
        if logfile.endswith('.log'):
            logfile.replace('.log', today + logend)
        else:
            logfile += today + logend
        logfilecount = 1
        while os.path.exists(logfile):
            logfile = logfile.replace('.' + str(logfilecount - 1), '')
            logfile = logfile + '.' + str(logfilecount)
            logfilecount += 1
            if logfilecount >= 60:
                raise SystemError('More than 1 logfile per second, this is insane.. aborting')

        fh = logging.FileHandler(logfile)
        fh.setFormatter(formatter)
        fh.setLevel(loglevel)
    logger.addHandler(ch)
    if logfile is not None:
        logger.addHandler(fh)
    sys.excepthook = exception_handler
    logger.propagate = False
    return logger