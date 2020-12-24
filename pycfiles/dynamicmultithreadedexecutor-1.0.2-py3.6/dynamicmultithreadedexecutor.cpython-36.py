# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/dynamicmultithreadedexecutor/dynamicmultithreadedexecutor.py
# Compiled at: 2017-12-28 17:04:39
# Size of source mod 2**32: 6490 bytes
import logging, time, six, threading
from six.moves.queue import Queue
import datetime, collections, inspect
from .finisher import finisher
from .worker import worker
from .utils import get_num_input_vars
LOGGER = logging.getLogger(__name__)

def execute_dynamic_multithreaded_task(iterable, thread_checker_func, poll_period, worker_function, output_queue_handler):
    """
    Execute a function for every item in iterable with a dynamic number of threads as defined by the return of thread_checker_func

    :type iterable: any iterable
    :type thread_checker_func: function with zero parameters and returns int of # of threads should be running
    :type poll_period: int
    :type worker_function: function with at least 1 parameter
    :type output_queue_handler: function with at least 1 parameter

    :param iterable: Iterable to pass into worker_function
    :param thread_checker_func: function that accepts no args and will return int for # of threads we should run
    :param poll_period: how often (in sec) we will run thread_checker_func
    :param worker_function: function that will be run multi-threaded and once per item in file_list
    :param output_queue_handler: consume things that worker_function returns. this will run single threaded, once per execution

    :rtype : None - output_queue_handler should handle all output functionality
    """
    LOGGER.info('starting dynamic multithreaded execution')
    if not isinstance(iterable, collections.Iterable):
        raise AssertionError
    else:
        if not callable(thread_checker_func):
            raise AssertionError
        else:
            assert isinstance(poll_period, six.integer_types)
            assert callable(worker_function)
        assert callable(output_queue_handler)
    LOGGER.info('all assertions passed, doing some checks on the callables passed in')
    if get_num_input_vars(worker_function) != 1:
        raise RuntimeError('worker_function must accept one and only one inputs')
    if get_num_input_vars(output_queue_handler) != 1:
        raise RuntimeError('output_queue_handler must accept one and only one inputs')
    if get_num_input_vars(thread_checker_func) != 0:
        raise RuntimeError('thread_checker_func must accept no inputs')
    LOGGER.info('callables appear to have ok inputs')
    inq = Queue()
    outq = Queue()
    deathq = Queue()
    kill_boolean = False
    LOGGER.info('loading up inq')
    inq.queue.extend(iterable)
    thread_list = []
    LOGGER.info('starting up finisher thread')
    fin_thread = threading.Thread(target=finisher, kwargs={'outq':outq,  'output_queue_handler':output_queue_handler,  'kill_boolean':kill_boolean})
    fin_thread.start()
    LOGGER.info('entering infinite loop (until job is done)')
    while True:
        last_run = datetime.datetime.now()
        if kill_boolean:
            LOGGER.debug('kill_boolean is true, we are going to stop now!')
            return
        if not inq.empty():
            target_threads = thread_checker_func()
            thread_list = [t for t in thread_list if t.is_alive()]
            while len(thread_list) < target_threads:
                LOGGER.debug('spinning up a new worker thread')
                base_kwargs = {'inq':inq,  'outq':outq,  'deathq':deathq,  'worker_function':worker_function,  'kill_boolean':kill_boolean}
                t = threading.Thread(target=worker, kwargs=base_kwargs)
                t.start()
                thread_list.append(t)

            thread_overage = len(thread_list) - target_threads
            for i in range(thread_overage):
                LOGGER.debug('sending death signal to deathq')
                deathq.put('DIE DIE DIE')

            while not deathq.empty():
                time.sleep(1)

            thread_list = [t for t in thread_list if t.is_alive()]
            LOGGER.debug('Currently have {} threads running'.format(len(thread_list)))
        else:
            thread_list = [t for t in thread_list if t.is_alive()]
            if not thread_list:
                print('All worker threads are done, killing finisher thread')
                outq.put('DIE DIE DIE')
                while fin_thread.is_alive():
                    print('finisher thread is still running, sleeping')
                    time.sleep(1)

                LOGGER.info('All threads have spun down, returning!')
                return
            LOGGER.info('inq is empty, but looks like we still have {} threads running, we will wait until all threads complete'.format(len(thread_list)))
        while (datetime.datetime.now() - last_run).total_seconds() < poll_period:
            time.sleep(1)