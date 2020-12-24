# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/log.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 5259 bytes
import logging, sys
from logging import DEBUG, INFO, WARNING, ERROR
FRAME = DEBUG - 5
LOG_NAMES = {'frame':FRAME,  'debug':DEBUG,  'info':INFO,  'warning':WARNING,  'error':ERROR}
SORTED_NAMES = tuple(k for k, v in sorted(LOG_NAMES.items()))
VERBOSE_FMT = '%(asctime)s,%(msecs)d %(levelname)-7s [%(filename)s:%(lineno)d] %(message)s'
DATE_FMT = '%d-%m-%Y:%H:%M:%S'

def add_arguments(parser):
    parser.add_argument('--loglevel',
      choices=SORTED_NAMES, default='info', help=LOGLEVEL_HELP)
    parser.add_argument('--verbose',
      '-v', action='store_true', help=VERBOSE_HELP)


def apply_args(args):
    if args.verbose:
        if args.loglevel != 'frame':
            logging.basicConfig(format=VERBOSE_FMT,
              datefmt=DATE_FMT,
              level=(logging.DEBUG))
    else:
        set_log_level(args.loglevel)


def _addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()
    else:
        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            (self._log)(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        (logging.log)(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def _new_custom_logger(name='BiblioPixel', fmt='%(levelname)s - %(module)s - %(message)s'):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=fmt)

    def add_handler(level, outfile):

        class Filter(logging.Filter):

            def filter(self, rec):
                return rec.levelno == level

        h = logging.StreamHandler(outfile)
        h.setLevel(level)
        h.addFilter(Filter())
        h.setFormatter(formatter)
        logger.addHandler(h)

    if not logger.handlers:
        logger.setLevel(INFO)
        add_handler(FRAME, sys.stdout)
        add_handler(DEBUG, sys.stdout)
        add_handler(INFO, sys.stdout)
        add_handler(WARNING, sys.stderr)
        add_handler(ERROR, sys.stderr)
    return logger


def set_log_level(level):
    """
    :param level: the level to set - either a string level name from
                  'frame', 'debug', 'info', 'warning', 'error'
                  or an integer log level from:
                  log.FRAME, log.DEBUG, log.INFO, log.WARNING, log.ERROR
    """
    if isinstance(level, str):
        level = LOG_NAMES[level.lower()]
    logger.setLevel(level)


def get_log_level():
    return logger.getEffectiveLevel()


def is_debug():
    return get_log_level() <= DEBUG


_addLoggingLevel('FRAME', FRAME)
logger = _new_custom_logger()
frame, debug, info, warning, error = (
 logger.frame, logger.debug, logger.info, logger.warning, logger.error)
printer = print
LOGLEVEL_HELP = 'Set what level of events to log. Higher log levels print less.'
VERBOSE_HELP = 'If this is set, then errors are reported with a full stack trace, and\nloglevel is by default set to debug\n'
from . import deprecated
if deprecated.allowed():

    def setLogLevel(level):
        deprecated.deprecated('util.setLogLevel')
        set_log_level(level)