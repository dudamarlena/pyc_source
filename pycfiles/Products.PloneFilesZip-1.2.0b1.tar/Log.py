# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\Log.py
# Compiled at: 2008-11-19 15:29:07
__doc__ = '\nOne can override the following variables :\n\nLOG_LEVEL : The log level, from 0 to 5.\nA Log level n implies all logs from 0 to n.\nLOG_LEVEL MUST BE OVERRIDEN !!!!!\n\n\nLOG_NONE = 0            => No log output\nLOG_CRITICAL = 1        => Critical problems (data consistency, module integrity, ...)\nLOG_ERROR = 2           => Error (runtime exceptions, ...)\nLOG_WARNING = 3         => Warning (non-blocking exceptions, ...)\nLOG_NOTICE = 4          => Notices (Special conditions, ...)\nLOG_DEBUG = 5           => Debug (Debugging information)\n\n\nLOG_PROCESSOR : A dictionnary holding, for each key, the data processor.\nA data processor is a function that takes only one parameter : the data to print.\nDefault : logFile for all keys.\n'
LOG_LEVEL = -1
LOG_NONE = 0
LOG_CRITICAL = 1
LOG_ERROR = 2
LOG_WARNING = 3
LOG_NOTICE = 4
LOG_DEBUG = 5
from sys import stdout, stderr, exc_info
import time, thread, threading, traceback, os, pprint
LOG_STACK_DEPTH = [
 -2]

def Log(level, *args):
    """
    Log(level, *args) => Pretty-prints data on the console with additional information.
    """
    if LOG_LEVEL and level <= LOG_LEVEL:
        if level not in LOG_PROCESSOR.keys():
            raise ValueError, 'Invalid log level :', level
        stack = ''
        stackItems = traceback.extract_stack()
        for depth in LOG_STACK_DEPTH:
            stackItem = stackItems[depth]
            stack = '%s%s:%s:' % (stack, os.path.basename(stackItem[0]), stackItem[1])

        pr = '%8s %s%s: ' % (LOG_LABEL[level], stack, time.ctime(time.time()))
        for data in args:
            try:
                if '\n' in data:
                    data = data
                else:
                    data = pprint.pformat(data)
            except:
                data = pprint.pformat(data)

            pr = pr + data + ' '

        LOG_PROCESSOR[level](level, LOG_LABEL[level], pr, stackItems)


def FormatStack(stack):
    """
    FormatStack(stack) => string
    
    Return a 'loggable' version of the stack trace
    """
    ret = ''
    for s in stack:
        ret = ret + '%s:%s:%s: %s\n' % (os.path.basename(s[0]), s[1], s[2], s[3])

    return ret


LOG_OUTPUT = stderr

def logFile(level, label, data, stack):
    """
    logFile : writes data to the LOG_OUTPUT file.
    """
    LOG_OUTPUT.write(data + '\n')
    LOG_OUTPUT.flush()


import zLOG
zLogLevelConverter = {LOG_NONE: zLOG.TRACE, LOG_CRITICAL: zLOG.PANIC, LOG_ERROR: zLOG.ERROR, LOG_WARNING: zLOG.PROBLEM, LOG_NOTICE: zLOG.INFO, LOG_DEBUG: zLOG.DEBUG}

def logZLog(level, label, data, stack):
    """
    logZLog : writes data though Zope's logging facility
    """
    zLOG.LOG('IngeniWeb', zLogLevelConverter[level], '', data + '\n')


LOG_PROCESSOR = {LOG_NONE: logZLog, LOG_CRITICAL: logZLog, LOG_ERROR: logZLog, LOG_WARNING: logZLog, LOG_NOTICE: logZLog, LOG_DEBUG: logFile}
LOG_LABEL = {LOG_NONE: '', LOG_CRITICAL: 'CRITICAL', LOG_ERROR: 'ERROR   ', LOG_WARNING: 'WARNING ', LOG_NOTICE: 'NOTICE  ', LOG_DEBUG: 'DEBUG   '}