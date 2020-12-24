# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\loggerHelpbylw.py
# Compiled at: 2019-12-26 00:48:38
# Size of source mod 2**32: 1325 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import logging, threading
initLock = threading.Lock()
rootLoggerInitialized = False
log_format = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
simpleLog_format = '%(message)s'
level = logging.INFO
file_log = None
console_log = True

def getFileLogger(name, fileName, mode_='w'):
    aLog = logging.getLogger(name)
    aLog.propagate = False
    if not aLog.hasHandlers():
        aLog.setLevel(logging.INFO)
        fileHandler = logging.FileHandler(fileName, mode=mode_)
        fileHandler.setFormatter(logging.Formatter(simpleLog_format))
        aLog.addHandler(fileHandler)
    return aLog