# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/logger/logger.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 3768 bytes
"""
HELP : to use this feature :
 - copy configuration sample file into your configuration directory
 - edit this configuration file (help links inside)
 - import modules :
    - from inspect import signature
    - from pythoncommontools.objectUtil.objectUtil import methodArgsStringRepresentation
    - from pythoncommontools.logger import logger
 - in method or function :
    - collect inputs arguments :
       - argsStr=methodArgsStringRepresentation(signature(<CLASS>.<METHOD>).parameters,locals())
       - argsStr=methodArgsStringRepresentation(signature(FUNCTION).parameters, locals())
    - use logger methods :
       - logger.loadedLogger.input (__name__, <CLASS>.__name__ ,<CLASS>.<METHOD>.__name__, message=argsStr)
       - logger.loadedLogger.output (__name__, <CLASS>.__name__ ,<CLASS>.<METHOD>.__name__, message=output)
       - logger.loadedLogger.input (__name__, functionOrmethod=FUNCTION.__name__, message=argsStr)
       - logger.loadedLogger.output (__name__, functionOrmethod=FUNCTION.__name__, message=output )
"""
import logging
from logging import Logger as DefaultLogger
from logging.config import fileConfig

def loadLogger(name, logConfigurationFilePath):
    loadedLogger = Logger(name, logConfigurationFilePath)
    return loadedLogger


class Logger(DefaultLogger):
    methodSeparator = '.'

    def input(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.info(self, 'INPUT - ' + Logger.format(moduleName, className, functionOrmethod, message))

    def output(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.info(self, 'OUTPUT - ' + Logger.format(moduleName, className, functionOrmethod, message))

    def debug(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.debug(self, Logger.format(moduleName, className, functionOrmethod, message))

    def info(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.info(self, Logger.format(moduleName, className, functionOrmethod, message))

    def warning(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.warning(self, Logger.format(moduleName, className, functionOrmethod, message))

    def error(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.error(self, Logger.format(moduleName, className, functionOrmethod, message))

    def critical(self, moduleName, className='', functionOrmethod='', message=''):
        DefaultLogger.critical(self, Logger.format(moduleName, className, functionOrmethod, message))

    @staticmethod
    def format(moduleName, className, functionOrmethod, rawMessage):
        formattedMessage = moduleName
        if len(className) > 0:
            formattedMessage = Logger.methodSeparator.join((formattedMessage, className))
        if len(functionOrmethod) > 0:
            formattedMessage = Logger.methodSeparator.join((formattedMessage, functionOrmethod))
        rawMessageStr = str(rawMessage)
        if len(rawMessageStr) > 0:
            formattedMessage = ' : '.join((formattedMessage, rawMessageStr))
        return formattedMessage

    def __init__(self, name, logConfigurationFilePath):
        fileConfig(logConfigurationFilePath)
        super().__init__(name)
        self.addHandler(logging.getLogger())