# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/pool/guipoolthread.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 7925 bytes
"""
Low-level **worker thread pool** (i.e., platform-portable, pure-Qt,
:class:`QThreadPool`-based container of one or more threads, each working
exactly one :class:`QRunnable`-based worker at a given time) classes.
"""
from PySide2.QtCore import QThreadPool
from betse.util.io.log import logs
from betse.util.type.iterable import itertest
from betse.util.type.types import type_check, IterableTypes
from betsee.guiexception import BetseePySideThreadException
from betsee.util.type.guitype import QThreadPoolOrNoneTypes
from betsee.util.thread.pool.guipoolwork import QBetseeThreadPoolWorker

@type_check
def die_if_working(thread_pool: QThreadPoolOrNoneTypes=None) -> None:
    """
    Raise an exception if one or more workers are currently working in one or
    more non-idle threads of the passed thread pool.

    Parameters
    ----------
    thread_pool : QThreadPoolOrNoneTypes
        Thread pool to run this worker in. Defaults to ``None``, in which case
        the singleton thread pool returned by the :func:`get_thread_pool`
        function is defaulted to.

    Raises
    ----------
    BetseePySideThreadException
        If one or more workers are currently working in one or more non-idle
        threads of this thread pool.

    See Also
    ----------
    :func:`is_working`
        Further details.
    """
    if is_working(thread_pool):
        worker_count = get_worker_count(thread_pool)
        raise BetseePySideThreadException('Thread pool contains {} working workers.'.format(worker_count))


@type_check
def is_working(thread_pool: QThreadPoolOrNoneTypes=None) -> bool:
    """
    ``True`` only if one or more workers are currently working in one or more
    non-idle threads of the passed thread pool.

    Parameters
    ----------
    thread_pool : QThreadPoolOrNoneTypes
        Thread pool to run this worker in. Defaults to ``None``, in which case
        the singleton thread pool returned by the :func:`get_thread_pool`
        function is defaulted to.
    """
    return get_worker_count(thread_pool) > 0


def get_thread_pool() -> QThreadPool:
    """
    Singleton **worker thread pool** (i.e., platform-portable, pure-Qt,
    :class:`QThreadPool`-based container of one or more threads, each working
    exactly one :class:`QRunnable`-based worker at a given time).

    This singleton is globally reusable across the entire application.
    """
    return QThreadPool.globalInstance()


@type_check
def get_worker_count(thread_pool: QThreadPoolOrNoneTypes=None) -> int:
    """
    Number of workers currently working in non-idle threads of the passed
    thread pool.

    Parameters
    ----------
    thread_pool : QThreadPoolOrNoneTypes
        Thread pool to inspect the wokers of. Defaults to ``None``, in which
        case the singleton thread pool returned by the :func:`get_thread_pool`
        function is defaulted to.
    """
    if thread_pool is None:
        thread_pool = get_thread_pool()
    return thread_pool.activeThreadCount()


@type_check
def start_worker(worker: QBetseeThreadPoolWorker, thread_pool: QThreadPoolOrNoneTypes=None) -> None:
    """
    Start the passed thread pool worker in the passed thread pool.

    Specifically, this function:

    * If this thread pool contains at least one idle thread:
      * Moves this worker from the original thread in which this worker was
        instantiated into this idle thread.
      * Calls the :meth:`QBetseeThreadPoolWorker.run` method of this worker.
      * Garbage collects this worker when this method returns.
    * Else, queues a request to subsequently run this worker in the next idle
      thread in this thread pool.

    Parameters
    ----------
    worker : QBetseeThreadPoolWorker
        Worker to be started in this thread pool.
    thread_pool : QThreadPoolOrNoneTypes
        Thread pool to start this worker in. Defaults to ``None``, in which
        case the singleton thread pool returned by the :func:`get_thread_pool`
        function is defaulted to.
    """
    if thread_pool is None:
        thread_pool = get_thread_pool()
    thread_pool.start(worker)


@type_check
def halt_workers(workers: IterableTypes, milliseconds: int, thread_pool: QThreadPoolOrNoneTypes=None) -> None:
    """
    Wait no more than the passed number of milliseconds for all passed thread
    pool workers in the passed thread pool to gracefully stop and, if one or
    more workers fail to do so, non-gracefully terminate these workers
    immediately.

    Specifically, this function tests whether one or more thread pool workers
    are still working *and* fail to stop (gracefully or otherwise) after
    blocking the caller's thread for the passed number of milliseconds; if this
    is the case, each such worker is terminated by any means necessary.

    Parameters
    ----------
    workers : IterableTypes
        Workers to be halted in this thread pool.
    milliseconds : int
        Number of milliseconds (i.e., 10^-3 seconds) to block the current
        thread *before* non-gracefully halting these workers.
    thread_pool : QThreadPoolOrNoneTypes
        Thread pool to halt these workers in. Defaults to ``None``, in which
        case the singleton thread pool returned by the :func:`get_thread_pool`
        function is defaulted to.
    """
    logs.log_debug('Halting thread pool...')
    itertest.die_unless_items_instance_of(iterable=workers,
      cls=QBetseeThreadPoolWorker)
    if thread_pool is None:
        thread_pool = get_thread_pool()
    if not is_working(thread_pool):
        return
    workers_num = len(workers)
    seconds = milliseconds * 0.001
    logs.log_warning('Waiting %g seconds for %d thread pool worker(s) to halt...', seconds, workers_num)
    if not thread_pool.waitForDone(milliseconds):
        logs.log_warning('Forcing %d thread pool worker(s) to halt...', workers_num)
        for worker in workers:
            worker.halt()