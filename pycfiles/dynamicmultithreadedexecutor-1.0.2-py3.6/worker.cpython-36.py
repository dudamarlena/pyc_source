# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/dynamicmultithreadedexecutor/worker.py
# Compiled at: 2017-12-28 17:05:11
# Size of source mod 2**32: 3354 bytes
from six.moves.queue import Queue, Empty
import six, threading, logging, traceback
from .utils import get_num_input_vars
from .exceptions import KillExecution
LOGGER = logging.getLogger(__name__)

def worker(inq, outq, deathq, worker_function, kill_boolean):
    """
    Worker function that is called once per item in inq but in a multithreaded manner

    Worker functions are spun up/down as needed based on how many threads the main dynamicmultithreaded object thinks we should have

    :rtype : None, although into outq we inject whatever is retruned from the worker_function, if worker_function raises an exception a dict with keys "exception" and "traceback" are returned

    :param inq: queue we will pull from to run worker_function
    :param outq: output queue we will put into with results from worker_function
    :param deathq: we pull from here every execution, if we get something we return and therefore kill off our thread
    :param worker_function: user provided function to execute
    :param kill_boolean: allows us to kill the whole execution from the worker raising a KillExecution exception

    :type inq: Queue
    :type outq: Queue
    :type deathq: Queue
    :type worker_function: callable
    :type kill_boolean: bool
    """
    if not isinstance(inq, Queue):
        raise AssertionError
    else:
        if not isinstance(outq, Queue):
            raise AssertionError
        else:
            if not isinstance(deathq, Queue):
                raise AssertionError
            elif not callable(worker_function):
                raise AssertionError
            assert isinstance(kill_boolean, bool)
        LOGGER.info('spinning up thread: {}'.format(threading.current_thread().name))
        if get_num_input_vars(worker_function) != 1:
            kill_boolean = True
            raise RuntimeError('worker function must take in at least one arg!')
    while True:
        try:
            _ = deathq.get(block=False)
        except Empty:
            pass
        else:
            LOGGER.info('spinning down thread: {} - got a death threat from deathq'.format(threading.current_thread().name))
            return
            if kill_boolean:
                LOGGER.info('spinning down thread: {} - got a death threat from kill_boolean'.format(threading.current_thread().name))
                return
            try:
                itm_to_run = inq.get(timeout=5)
            except Empty:
                LOGGER.info('inQ is empty, thread {} returning'.format(threading.current_thread().name))
                return
            else:
                try:
                    response = worker_function(itm_to_run)
                    output = {'execution_success':True, 
                     'task_output':response}
                except KillExecution:
                    LOGGER.warning('we got a KillExecution exception, killing off our execution and returning')
                    kill_boolean = True
                    return
                except Exception as e:
                    tb = traceback.format_exec()
                    output = {'execution_success':False, 
                     'exception_message':str(e), 
                     'traceback':tb}

                outq.put(output)
                LOGGER.debug('work is done, putting into outq!')