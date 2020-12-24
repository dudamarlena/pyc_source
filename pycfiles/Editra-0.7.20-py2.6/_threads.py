# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/_threads.py
# Compiled at: 2011-04-10 13:31:48
"""
Editra Business Model Library: ThreadPool

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _threads.py 67422 2011-04-09 17:23:27Z CJP $'
__revision__ = '$Revision: 67422 $'
__all__ = [
 'ThreadPool']
import threading, Queue

class ThreadPool(object):
    """Object for managing a collection of threads and dispatching jobs
    to them.

    """

    def __init__(self, tcount, qsize=-1):
        """Create the ThreadPool
        @param tcount: max number of threads to keep in the pool
        @keyword qsize: size of job queue (-1 for unlimited)

        """
        super(ThreadPool, self).__init__()
        self._poolsize = tcount
        self._jobs = Queue.Queue(qsize)
        self._threads = [ _WorkerThread(self._jobs) for t in range(self._poolsize) ]

    ThreadCount = property(lambda self: self._poolsize)
    JobCount = property(lambda self: self._jobs.qsize())

    def QueueJob(self, funct, *args, **kwargs):
        """Add a job to be processed
        @param funct: callable
        @param args: list of any positional arguments to funct
        @param kwargs: map of any keyword arguments to funct

        """
        assert callable(funct)
        self._jobs.put((funct, args, kwargs))

    def Shutdown(self):
        """Shutdown the ThreadPool
        @note: Blocking call until all threads have exited

        """
        self._jobs.join()


class _WorkerThread(threading.Thread):
    """Worker thread class to be used by the ThreadPool"""

    def __init__(self, jobs):
        """Create the Thread object
        @param jobs: Queue object

        """
        super(_WorkerThread, self).__init__()
        self._jobs = jobs
        self.daemon = True
        self.start()

    def run(self):
        """Run and process jobs until requested to exit"""
        while True:
            (funct, args, kwargs) = self._jobs.get()
            try:
                try:
                    funct(*args, **kwargs)
                except Exception, msg:
                    pass

            finally:
                self._jobs.task_done()


if __name__ == '__main__':
    pool = ThreadPool(5)
    import time, random

    def Job(id_, length):
        print 'JOB: %d, begin' % id_
        time.sleep(length)
        print 'JOB: %d, end' % id_


    print 'Start Jobs'
    for x in range(8):
        pool.QueueJob(Job, x, random.randint(1, 20))

    print 'All Jobs Queued'
    pool.Shutdown()
    print 'All Done!'