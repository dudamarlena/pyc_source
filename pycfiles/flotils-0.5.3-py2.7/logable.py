# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flotils\logable.py
# Compiled at: 2019-04-14 10:12:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'the01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2013-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.6'
__date__ = b'2019-03-21'
import logging, inspect
try:
    import colorlog
except ImportError:
    colorlog = None

TIMEFORMAT_DEFAULT = b'%Y-%m-%d %H:%M:%S'

class FunctionFilter(logging.Filter):
    """
    Add an extra 'function' if not already present
    """

    def filter(self, record):
        if not hasattr(record, b'function'):
            record.function = b''
        else:
            fct = record.function
            if fct and not fct.startswith(b'.'):
                record.function = b'.' + fct
        return True


class Logable(object):
    """
    Class to facilitate clean logging with class/function/id information
    """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Logable, self).__init__()
        self._id = settings.get(b'id', None)
        self._logger = logging.getLogger(self.name)
        return

    @property
    def name(self):
        """
        Get the module name

        :return: Module name
        :rtype: str | unicode
        """
        res = type(self).__name__
        if self._id:
            res += (b'.{}').format(self._id)
        return res

    def _get_function_name(self):
        """
        Get function name of calling method

        :return: The name of the calling function
            (expected to be called in self.error/debug/..)
        :rtype: str | unicode
        """
        fname = inspect.getframeinfo(inspect.stack()[2][0]).function
        if fname == b'<module>':
            return b''
        else:
            return fname

    def log(self, level, msg, *args, **kargs):
        self._logger.log(level, msg, extra={b'function': self._get_function_name()}, *args, **kargs)

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self._logger.fatal(msg, extra={b'function': self._get_function_name()}, *args, **kwargs)


class ModuleLogable(Logable):
    """ Class to log on module level """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(ModuleLogable, self).__init__(settings)
        return

    @property
    def name(self):
        return self.__module__


def get_logger():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    if mod is None:
        logging.error(dir(frm))
        logging.error(dir(inspect.stack()[0]))

    class TempLogable(Logable):
        """ Class to log on module level """

        def __init__(self, settings=None):
            if settings is None:
                settings = {}
            super(TempLogable, self).__init__(settings)
            return

        @property
        def name(self):
            if mod is None:
                return b''
            else:
                return mod.__name__

    logger = TempLogable()
    return logger


default_logging_config = {b'version': 1, 
   b'disable_existing_loggers': False, 
   b'formatters': {b'threaded': {b'format': b'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}, 
                   b'verbose': {b'format': b'%(asctime)s %(levelname)-8s [%(name)s%(function)s] %(message)s', 
                                b'datefmt': b'%Y-%m-%d %H:%M:%S'}, 
                   b'colored': {b'()': b'colorlog.ColoredFormatter', 
                                b'format': b'%(blue,bold)s%(asctime)s%(reset)s %(log_color)s%(levelname)-8s%(reset)s%(blue)s[%(name)s%(function)s]%(reset)s %(message_log_color)s%(message)s', 
                                b'datefmt': b'%Y-%m-%d %H:%M:%S', 
                                b'log_colors': {b'DEBUG': b'cyan', 
                                                b'INFO': b'green', 
                                                b'WARNING': b'white,bg_yellow', 
                                                b'ERROR': b'yellow,bg_red', 
                                                b'CRITICAL': b'yellow,bg_red'}, 
                                b'secondary_log_colors': {b'message': {b'DEBUG': b'cyan', 
                                                                       b'INFO': b'green', 
                                                                       b'WARNING': b'yellow', 
                                                                       b'ERROR': b'red', 
                                                                       b'CRITICAL': b'red,bg_white'}}}, 
                   b'simple': {b'format': b'%(levelname)s %(message)s'}}, 
   b'filters': {b'my': {b'()': b'flotils.logable.FunctionFilter'}}, 
   b'handlers': {b'null': {b'level': b'DEBUG', 
                           b'class': b'logging.NullHandler', 
                           b'filters': [
                                      b'my']}, 
                 b'console': {b'level': b'DEBUG', 
                              b'class': b'logging.StreamHandler', 
                              b'formatter': b'colored', 
                              b'filters': [
                                         b'my']}}, 
   b'loggers': {b'': {b'handlers': [
                                  b'console'], 
                      b'propagate': True, 
                      b'level': b'INFO'}}}
if colorlog is None:
    del default_logging_config[b'formatters'][b'colored']
    default_logging_config[b'handlers'][b'console'][b'formatter'] = b'verbose'