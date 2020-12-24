# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/futures.py
# Compiled at: 2012-07-26 02:07:58
import atexit, threading, weakref, math
try:
    import queue
except ImportError:
    import Queue as queue

try:
    from concurrent import futures
except ImportError:
    raise ImportError('You must install the futures package to use the dynamic scaling thread pool.')

__all__ = [
 'ScalingPoolExecutor']
log = __import__('logging').getLogger(__name__)

def thread_worker(executor, jobs, timeout, maximum):
    i = maximum + 1
    try:
        while 1:
            if i:
                i -= 1
                try:
                    work = jobs.get(True, timeout)
                    if work is None:
                        runner = executor()
                        if runner is None or runner._shutdown:
                            log.debug('Worker instructed to shut down.')
                            break
                        del runner
                        continue
                except queue.Empty:
                    log.debug('Worker death from starvation.')
                    break
                else:
                    work.run()

        else:
            log.debug('Worker death from exhaustion.')

    except:
        log.critical('Unhandled exception in worker.', exc_info=True)

    runner = executor()
    if runner:
        runner._threads.discard(threading.current_thread())
    return


class ScalingPoolExecutor(futures.ThreadPoolExecutor):

    def __init__(self, workers, divisor, timeout):
        self._max_workers = workers
        self.divisor = divisor
        self.timeout = timeout
        self._work_queue = queue.Queue()
        self._threads = set()
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._management_lock = threading.Lock()
        atexit.register(self._atexit)

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            for i in range(len(self._threads)):
                self._work_queue.put(None)

        if wait:
            for thread in list(self._threads):
                thread.join()

        return

    def _atexit(self):
        self.shutdown(True)

    def _spawn(self):
        t = threading.Thread(target=thread_worker, args=(weakref.ref(self), self._work_queue, self.divisor, self.timeout))
        t.daemon = True
        t.start()
        with self._management_lock:
            self._threads.add(t)

    def _adjust_thread_count(self):
        pool = len(self._threads)
        if pool < self._optimum_workers:
            tospawn = int(self._optimum_workers - pool)
            log.debug('Spawning %d thread%s.' % (tospawn, tospawn != 1 and 's' or ''))
            for i in range(tospawn):
                self._spawn()

    @property
    def _optimum_workers(self):
        return min(self._max_workers, math.ceil(self._work_queue.qsize() / float(self.divisor)))