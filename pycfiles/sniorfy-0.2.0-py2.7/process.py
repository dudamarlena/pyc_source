# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sniorfy/process.py
# Compiled at: 2012-05-08 21:53:05
"""Utilities for working with multiple processes."""
from __future__ import absolute_import, division, with_statement
import errno, logging, os, sys, time, multiprocessing
from binascii import hexlify
from sniorfy import ioloop

def cpu_count():
    """Returns the number of processors on this machine."""
    if multiprocessing is not None:
        try:
            return multiprocessing.cpu_count()
        except NotImplementedError:
            pass

    try:
        return os.sysconf('SC_NPROCESSORS_CONF')
    except ValueError:
        pass

    logging.error('Could not detect number of processors; assuming 1')
    return 1


def _reseed_random():
    if 'random' not in sys.modules:
        return
    import random
    try:
        seed = long(hexlify(os.urandom(16)), 16)
    except NotImplementedError:
        seed = int(time.time() * 1000) ^ os.getpid()

    random.seed(seed)


_task_id = None

def fork_processes(num_processes, max_restarts=100):
    """Starts multiple worker processes.

    If ``num_processes`` is None or <= 0, we detect the number of cores
    available on this machine and fork that number of child
    processes. If ``num_processes`` is given and > 0, we fork that
    specific number of sub-processes.

    Since we use processes and not threads, there is no shared memory
    between any server code.

    Note that multiple processes are not compatible with the autoreload
    module (or the debug=True option to `tornado.web.Application`).
    When using multiple processes, no IOLoops can be created or
    referenced until after the call to ``fork_processes``.

    In each child process, ``fork_processes`` returns its *task id*, a
    number between 0 and ``num_processes``.  Processes that exit
    abnormally (due to a signal or non-zero exit status) are restarted
    with the same id (up to ``max_restarts`` times).  In the parent
    process, ``fork_processes`` returns None if all child processes
    have exited normally, but will otherwise only exit by throwing an
    exception.
    """
    global _task_id
    assert _task_id is None
    if num_processes is None or num_processes <= 0:
        num_processes = cpu_count()
    if ioloop.IOLoop.initialized():
        raise RuntimeError('Cannot run in multiple processes: IOLoop instance has already been initialized. You cannot call IOLoop.instance() before calling start_processes()')
    logging.info('Starting %d processes', num_processes)
    children = {}

    def start_child(i):
        global _task_id
        pid = os.fork()
        if pid == 0:
            _reseed_random()
            _task_id = i
            return i
        else:
            children[pid] = i
            return
            return

    for i in range(num_processes):
        id = start_child(i)
        if id is not None:
            return id

    num_restarts = 0
    while children:
        try:
            pid, status = os.wait()
        except OSError as e:
            if e.errno == errno.EINTR:
                continue
            raise

        if pid not in children:
            continue
        id = children.pop(pid)
        if os.WIFSIGNALED(status):
            logging.warning('child %d (pid %d) killed by signal %d, restarting', id, pid, os.WTERMSIG(status))
        else:
            if os.WEXITSTATUS(status) != 0:
                logging.warning('child %d (pid %d) exited with status %d, restarting', id, pid, os.WEXITSTATUS(status))
            else:
                logging.info('child %d (pid %d) exited normally', id, pid)
                continue
            num_restarts += 1
            if num_restarts > max_restarts:
                raise RuntimeError('Too many child restarts, giving up')
            new_id = start_child(id)
            if new_id is not None:
                return new_id

    sys.exit(0)
    return


def task_id():
    """Returns the current task id, if any.

    Returns None if this process was not created by `fork_processes`.
    """
    return _task_id