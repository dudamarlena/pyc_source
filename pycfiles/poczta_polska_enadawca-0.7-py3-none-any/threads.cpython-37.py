# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/threads.py
# Compiled at: 2019-11-11 22:57:25
# Size of source mod 2**32: 3251 bytes
import time, threading, traceback
from pocsuite3.lib.core.data import conf
from pocsuite3.lib.core.data import kb
from pocsuite3.lib.core.data import logger
from pocsuite3.lib.core.exception import PocsuiteConnectionException
from pocsuite3.lib.core.exception import PocsuiteThreadException
from pocsuite3.lib.core.exception import PocsuiteUserQuitException
from pocsuite3.lib.core.exception import PocsuiteValueException
from pocsuite3.lib.core.settings import MAX_NUMBER_OF_THREADS

def exception_handled_function(thread_function, args=(), silent=False):
    try:
        thread_function(*args)
    except KeyboardInterrupt:
        kb.thread_continue = False
        kb.thread_exception = True
        raise
    except Exception as ex:
        try:
            if not silent:
                logger.error('thread {0}: {1}'.format(threading.currentThread().getName(), str(ex)))
                if conf.verbose > 1:
                    traceback.print_exc()
        finally:
            ex = None
            del ex


def run_threads(num_threads, thread_function, args: tuple=(), forward_exception=True, start_msg=True):
    threads = []
    kb.multi_thread_mode = True
    kb.thread_continue = True
    kb.thread_exception = False
    try:
        try:
            if num_threads > 1:
                if start_msg:
                    info_msg = 'starting {0} threads'.format(num_threads)
                    logger.info(info_msg)
                if num_threads > MAX_NUMBER_OF_THREADS:
                    warn_msg = 'starting {0} threads, more than MAX_NUMBER_OF_THREADS:{1}'.format(num_threads, MAX_NUMBER_OF_THREADS)
                    logger.warn(warn_msg)
            else:
                thread_function()
                return
            for num_threads in range(num_threads):
                thread = threading.Thread(target=exception_handled_function, name=(str(num_threads)), args=(
                 thread_function, args))
                thread.setDaemon(True)
                try:
                    thread.start()
                except Exception as ex:
                    try:
                        err_msg = "error occurred while starting new thread ('{0}')".format(str(ex))
                        logger.critical(err_msg)
                        break
                    finally:
                        ex = None
                        del ex

                threads.append(thread)

            alive = True
            while alive:
                alive = False
                for thread in threads:
                    if thread.isAlive():
                        alive = True
                        time.sleep(0.1)

        except (KeyboardInterrupt, PocsuiteUserQuitException) as ex:
            try:
                kb.thread_continue = False
                kb.thread_exception = True
                logger.info('user aborted (Ctrl+C was pressed multiple times')
                if forward_exception:
                    return
            finally:
                ex = None
                del ex

        except (PocsuiteConnectionException, PocsuiteValueException) as ex:
            try:
                kb.thread_exception = True
                logger.error('thread {0}: {1}'.format(threading.currentThread().getName(), str(ex)))
                if conf.verbose > 1:
                    traceback.print_exc()
            finally:
                ex = None
                del ex

        except Exception as ex:
            try:
                kb.thread_exception = True
                logger.error('thread {0}: {1}'.format(threading.currentThread().getName(), str(ex)))
                traceback.print_exc()
            finally:
                ex = None
                del ex

    finally:
        kb.multi_thread_mode = False
        kb.thread_continue = True
        kb.thread_exception = False