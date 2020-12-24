# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/threadpool.py
# Compiled at: 2009-10-07 18:08:46
"""
Supply a ThreadPool, dispatching work to different threads.
"""
import sys, threading, Queue

class Error(Exception):
    """ General threadpool error """
    __module__ = __name__


class _DismissalLetter:
    """ Sent to a worker thread to dismiss it """
    __module__ = __name__


class ThreadPool(object):
    """ I'm a simple thread pool using constant size.

    To run a function in a thread, call dispatch() with a callable and
    optional arguments and keywords. callable must be thread safe!
    
    Usage::

        p = ThreadPool(10)
        p.start()
        try:
            p.dispatch(callable, foo, bar="baz")
            ...
        finally:
            p.stop()

    The pool keeps a constant number of worker threads active while its
    running, and dismiss all of them when you stop it. The pool can be
    stopped and started as needed. Before exiting the application, the
    pool must be stopped. Use try finally to make sure your app will
    quit.

    You can resize the pool while its running by modifying the size
    attribute.

    Unhandled exceptions in code executed by worker threads are printed
    to the pool logFile, defaulting to sys.stderr.

    The pool itself is NOT thread safe, and should be accessed by only
    one thread.
    """
    __module__ = __name__

    def __init__(self, size=10, logFile=None):
        """ Initialize a pool
        
        @param size: number of threads to employ.
        @param logFile: where exceptions go (default to sys.stderr)
        """
        self._queue = Queue.Queue()
        self._workers = []
        self._running = False
        self.setSize(size)
        self.logFile = logFile or sys.stderr

    def start(self):
        """ Start a pool with size worker threads.

        Raise threadpool.Error if the pool is already running.
        """
        if self._running:
            raise Error('the pool is already running.')
        for worker in range(self._size):
            self._employWorker()

        self._running = True

    def stop(self):
        """ Stop a pool. All workers are dismissed.

        Will block until all the workers finished their assignment,
        which can take some time.

        Raise threadpool.Error if the pool is not running.
        """
        if not self._running:
            raise Error('the pool is not running.')
        workers = self._workers[:]
        for worker in workers:
            self._dismissWorker()

        for worker in workers:
            worker.join()

        self._running = False

    def dispatch(self, callable, *args, **kw):
        """ Add callable to the work queue.

        Raise threadpool.Error if the pool is not running.

        @param callable: a callable
        @param args: arguments for callable
        @param kw: keyword arguments for callable
        """
        if not self._running:
            raise Error('the pool is not running.')
        self._queue.put((callable, args, kw))

    running = property(lambda self: self._running)

    def setSize(self, count):
        assert count >= 1, 'at least one worker threads must be employed'
        self._size = count
        if self._running:
            self.stop()
            self.start()

    size = property(lambda self: self._size, setSize, doc='number of worker threads')
    workers = property(lambda self: len(self._workers))

    def queueEmpty(self):
        """ Return True if the queue is empty, False otherwise.

        Because of multithreading semantics, this is not reliable.
        """
        return self._queue.empty()

    def _workerMainLoop(self):
        """ Loop forever, trying to get work from, the queue. """
        me = threading.currentThread()
        while 1:
            (callable, args, kw) = self._queue.get()
            if callable is _DismissalLetter:
                break
            try:
                callable(*args, **kw)
            except:
                import traceback
                traceback.print_exc(file=self.logFile)

            del callable
            del args
            del kw

        self._workers.remove(me)

    def _employWorker(self):
        t = threading.Thread(target=self._workerMainLoop)
        self._workers.append(t)
        t.start()

    def _dismissWorker(self):
        """ Dismiss the unfortunate next waiting worker """
        self.dispatch(_DismissalLetter)