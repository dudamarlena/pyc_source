# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-mybase/mybase/base.py
# Compiled at: 2019-01-28 02:09:05
import rootpath
rootpath.append()
import re, json, logging, coloredlogs, mybad
from os import environ as env
DISABLED_LOGLEVEL = 1000
DEFAULT_BASE_LOGGER = True
DEFAULT_BASE_LOGGER_FORMAT = '[%(name)s]: %(message)s'
DEFAULT_BASE_LOGGER_COLORS = True

class MyBaseError(mybad.Error):
    pass


class MyBase(object):

    def __init__(self, logger=None):
        logger = self._get_logger(logger)
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __bool__(self):
        return True

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return ('<{classname} logger={logger}>').format(classname=self.__class__.__name__, logger=bool(self.logger))

    def __str__(self):
        return ('<{classname} logger={logger}>').format(classname=self.__class__.__name__, logger=bool(self.logger))

    def _get_logger(self, logger=None):
        prefix = ('{name}').format(name=self.__class__.__name__)
        if logger is None:
            logger = logger or DEFAULT_BASE_LOGGER
        logging.basicConfig(format=DEFAULT_BASE_LOGGER_FORMAT)
        if logger == False:
            logger = logging.getLogger(prefix)
            logger.setLevel(DISABLED_LOGLEVEL)
        elif logger == True:
            logger = logging.getLogger(prefix)
        else:
            logger = logger
        colors = env.get('LOGGER_COLORS', None)
        colors = colors or env.get('COLORS', None)
        if colors is None:
            colors = DEFAULT_BASE_LOGGER_COLORS
        colors = re.search('^true|1$', str(colors), flags=re.IGNORECASE)
        if colors is None:
            colors = DEFAULT_BASE_LOGGER_COLORS
        if colors:
            coloredlogs.install(fmt=DEFAULT_BASE_LOGGER_FORMAT, logger=logger)
        return logger


Base = MyBase
BaseError = MyBaseError