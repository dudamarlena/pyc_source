# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/threads.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import time, threading, traceback
from thread import error as threadError
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import kb
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.lib.core.settings import PYVERSION
from pocsuite.lib.core.exception import PocsuiteConnectionException
from pocsuite.lib.core.exception import PocsuiteThreadException
from pocsuite.lib.core.exception import PocsuiteValueException

def runThreads(numThreads, threadFunction, forwardException=True, startThreadMsg=True):
    threads = []
    kb.multiThreadMode = True
    kb.threadContinue = True
    kb.threadException = False
    try:
        try:
            if numThreads > 1:
                if startThreadMsg:
                    infoMsg = 'starting %d threads' % numThreads
                    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
            else:
                threadFunction()
                return
            for numThread in xrange(numThreads):
                thread = threading.Thread(target=exceptionHandledFunction, name=str(numThread), args=[threadFunction])
                setDaemon(thread)
                try:
                    thread.start()
                except threadError as errMsg:
                    errMsg = "error occurred while starting new thread ('%s')" % errMsg
                    logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                    break

                threads.append(thread)

            alive = True
            while alive:
                alive = False
                for thread in threads:
                    if thread.isAlive():
                        alive = True
                        time.sleep(0.1)

        except KeyboardInterrupt:
            print
            kb.threadContinue = False
            kb.threadException = True
            if numThreads > 1:
                logger.log(CUSTOM_LOGGING.SYSINFO, 'waiting for threads to finish (Ctrl+C was pressed)')
            try:
                while threading.activeCount() > 1:
                    pass

            except KeyboardInterrupt:
                raise PocsuiteThreadException('user aborted (Ctrl+C was pressed multiple times)')

            if forwardException:
                raise
        except (PocsuiteConnectionException, PocsuiteValueException) as errMsg:
            print
            kb.threadException = True
            logger.log(CUSTOM_LOGGING.ERROR, 'thread %s: %s' % (threading.currentThread().getName(), errMsg))
        except:
            from pocsuite.lib.core.common import unhandledExceptionMessage
            print
            kb.threadException = True
            errMsg = unhandledExceptionMessage()
            logger.log(CUSTOM_LOGGING.ERROR, 'thread %s: %s' % (threading.currentThread().getName(), errMsg))
            traceback.print_exc()

    finally:
        kb.multiThreadMode = False
        kb.bruteMode = False
        kb.threadContinue = True
        kb.threadException = False


def setDaemon(thread):
    if PYVERSION >= '2.6':
        thread.daemon = True
    else:
        thread.setDaemon(True)


def exceptionHandledFunction(threadFunction):
    try:
        threadFunction()
    except KeyboardInterrupt:
        kb.threadContinue = False
        kb.threadException = True
        raise
    except Exception as errMsg:
        logger.log(CUSTOM_LOGGING.ERROR, 'thread %s: %s' % (threading.currentThread().getName(), errMsg))