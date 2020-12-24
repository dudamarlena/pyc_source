# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\henrio\workers.py
# Compiled at: 2017-12-19 19:57:46
# Size of source mod 2**32: 2851 bytes
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
from types import coroutine
from functools import partial
from .yields import get_loop
from .locks import Semaphore
from . import Conditional, Future
__all__ = [
 'threadworker', 'async_threadworker', 'processworker', 'async_processworker', 'AsyncFuture']

@coroutine
def async_worker(pooltype, func, *args, **kwargs):
    """Will run an async function with the given args in another thread or process using the loop's pool.
     1 for processpool, 0 for threadpool"""
    fut = Future()
    loop = yield from get_loop()

    def runner():
        coro = func(*args, **kwargs)
        l = type(loop)()
        return l.run_until_complete(coro)

    pool = get_pool(pooltype, loop)
    pool.apply_async(runner, callback=(fut.set_result), error_callback=(fut.set_exception))
    res = yield from fut
    return res
    if False:
        yield None


@coroutine
def worker(pooltype, func, *args, **kwargs):
    """Will run an sync function with the given args in another thread or process using the loop's pool.
     1 for processpool, 0 for threadpool"""
    fut = Future()
    loop = yield from get_loop()
    pool = get_pool(pooltype, loop)
    pool.apply_async(func, args=args, kwds=kwargs, callback=(fut.set_result), error_callback=(fut.set_exception))
    res = yield from fut
    return res
    if False:
        yield None


def get_pool(pooltype, loop):
    """Will get the pool from a loop given the type, quick util"""
    if pooltype:
        if loop.processpool:
            pool = loop.processpool
        else:
            pool = loop.processpool = ProcessPool()
    else:
        if loop.threadpool:
            pool = loop.threadpool
        else:
            pool = loop.threadpool = ThreadPool()
    return pool


threadworker = partial(worker, 0)
processworker = partial(worker, 1)
async_threadworker = partial(async_worker, 0)
async_processworker = partial(async_worker, 1)

async def AsyncFuture(async_result):
    """Meant to wrap a `multiprocessing.pool.ApplyResult`. Returns a conditional that waits for the result to be ready"""
    cond = Conditional(async_result.ready)
    cond.add_done_callback(async_result.get)
    return await cond


class Pool:

    def __init__(self, factory, workers):
        self.waiter = Semaphore(workers)
        self.factory = factory
        self.workers = [factory() for _ in range(workers)]

    def shutdown(self):
        for worker in self.workers:
            worker.shutdown()

        self.workers = []

    async def acquire(self):
        await self.waiter.acquire()
        return self.workers.pop()

    async def release(self, worker):
        await self.waiter.release()
        self.workers.append(worker)