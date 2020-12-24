# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/multiprocess.py
# Compiled at: 2018-04-23 11:23:30
# Size of source mod 2**32: 4642 bytes
import multiprocessing.dummy as multiprocessing
import sys
import rumba.log as log
if sys.version_info[0] >= 3:
    import contextlib
else:
    import contextlib2 as contextlib
logger = log.get_logger(__name__)

def call_in_parallel(name_list, argument_list, executor_list):
    """
    Calls each executor in executor_list with the corresponding
    argument in argument_list

    Assumes that the three lists are the same length, will fail otherwise.
    Is equivalent to
    for i, e in enumerate(executor_list):
        e(argument_list[i])
    but all calls will be executed in parallel.

    If successful, no output will be given. Otherwise, this will raise
    the exception raised by one failed call at random.

    :param name_list: list of names of the executors (used for logging)
    :param argument_list: list of arguments to the executors
    :param executor_list: list of executors (as functions)
    """
    if len(executor_list) != len(name_list) or len(executor_list) != len(argument_list):
        raise ValueError('Names, arguments and executors lists must have the same length')

    def job(executor, name, m_queue, argument):
        try:
            logger.debug('Starting process "%s".' % (
             name,))
            executor(argument)
            m_queue.put('DONE')
        except BaseException as e:
            try:
                logger.error('Setup failed. %s: %s', type(e).__name__, str(e))
                m_queue.put(e)
            finally:
                e = None
                del e

    logger.debug('About to start spawning processes.')
    queue = multiprocessing.Queue()
    with contextlib.ExitStack() as (stack):
        msg_to_be_read = 0
        for i, e in enumerate(executor_list):
            stack.enter_context(ProcessContextManager(target=job,
              args=(
             e, name_list[i], queue, argument_list[i])))
            msg_to_be_read += 1

        results = []
        for _ in range(len(executor_list)):
            result = queue.get()
            msg_to_be_read -= 1
            results.append(result)

        for result in results:
            if result != 'DONE':
                raise result


class ProcessContextManager(object):

    def __init__(self, target, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        self.process = multiprocessing.Process(target=target,
          args=(tuple(args)),
          kwargs=kwargs)

    def __enter__(self):
        self.process.start()
        return self.process

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None or exc_val is not None or exc_tb is not None:
            logger.error('Subprocess error: %s.' % (type(exc_val).__name__,))
            try:
                self.process.terminate()
                self.process.join()
            except AttributeError:
                pass

            return False
        self.process.join()
        return True