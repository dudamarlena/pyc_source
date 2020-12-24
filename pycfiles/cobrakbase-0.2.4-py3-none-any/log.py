# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/utils/log.py
# Compiled at: 2016-08-05 06:16:57
import os, sys, time, logging, logging.handlers
from utils import config
__all__ = [
 'set_logger', 'debug', 'info', 'warning', 'error',
 'critical', 'exception']
COLOR_RED = '\x1b[1;31m'
COLOR_GREEN = '\x1b[1;32m'
COLOR_YELLOW = '\x1b[1;33m'
COLOR_BLUE = '\x1b[1;34m'
COLOR_PURPLE = '\x1b[1;35m'
COLOR_CYAN = '\x1b[1;36m'
COLOR_GRAY = '\x1b[1;37m'
COLOR_WHITE = '\x1b[1;38m'
COLOR_RESET = '\x1b[1;0m'
LOG_COLORS = {'DEBUG': '%s', 
   'INFO': COLOR_GREEN + '%s' + COLOR_RESET, 
   'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET, 
   'ERROR': COLOR_RED + '%s' + COLOR_RESET, 
   'CRITICAL': COLOR_RED + '%s' + COLOR_RESET, 
   'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET}
g_logger = None

class ColoredFormatter(logging.Formatter):
    """A colorful formatter."""

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return LOG_COLORS.get(level_name, '%s') % msg


def add_handler(cls, level, fmt, colorful, **kwargs):
    """Add a configured handler to the global logger."""
    global g_logger
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)
    handler = cls(**kwargs)
    handler.setLevel(level)
    if colorful:
        formatter = ColoredFormatter(fmt)
    else:
        formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    g_logger.addHandler(handler)
    return handler


def add_stream_handler(level, fmt):
    """Add a stream handler to the global logger."""
    return add_handler(logging.StreamHandler, level, fmt, True)


def add_file_handler(level, fmt, filename, mode, backup_count, limit, when):
    """Add a file handler to the global logger."""
    kwargs = {}
    if filename is None:
        logs_directory = config.Config('cobra', 'logs_directory').value
        if os.path.isdir(logs_directory) is not True:
            os.mkdir(logs_directory)
        filename = logs_directory + os.sep + time.strftime('%Y-%m-%d') + '.log'
    kwargs['filename'] = filename
    if backup_count == 0:
        cls = logging.FileHandler
        kwargs['mode'] = mode
    elif when is None:
        cls = logging.handlers.RotatingFileHandler
        kwargs['maxBytes'] = limit
        kwargs['backupCount'] = backup_count
        kwargs['mode'] = mode
    else:
        cls = logging.handlers.TimedRotatingFileHandler
        kwargs['when'] = when
        kwargs['interval'] = limit
        kwargs['backupCount'] = backup_count
    return add_handler(cls, level, fmt, False, **kwargs)


def init_logger():
    """Reload the global logger."""
    global g_logger
    if g_logger is None:
        g_logger = logging.getLogger()
    else:
        logging.shutdown()
        g_logger.handlers = []
    g_logger.setLevel(logging.DEBUG)
    return


def set_logger(filename=None, mode='a', level='DEBUG:INFO', fmt=None, backup_count=5, limit=20480, when=None):
    """Configure the global logger."""
    level = level.split(':')
    if len(level) == 1:
        s_level = f_level = level[0]
    else:
        s_level = level[0]
        f_level = level[1]
    if fmt is not None:
        if s_level == 'ERROR' or f_level == 'ERROR':
            fmt = "[%(levelname)s] %(asctime)s %(message)s in  '%(filename)s:%(lineno)s'"
        else:
            fmt = '[%(levelname)s] %(asctime)s %(message)s'
    init_logger()
    add_stream_handler(s_level, fmt)
    add_file_handler(f_level, fmt, filename, mode, backup_count, limit, when)
    import_log_funcs()
    return


def import_log_funcs():
    """Import the common log functions from the global logger to the module."""
    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
     'exception']
    for func_name in log_funcs:
        func = getattr(g_logger, func_name)
        setattr(curr_mod, func_name, func)


set_logger()