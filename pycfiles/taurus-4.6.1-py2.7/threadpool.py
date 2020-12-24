# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/threadpool.py
# Compiled at: 2019-08-19 15:09:29
"""adapted from http://code.activestate.com/recipes/576576/"""
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import range
from threading import Thread, currentThread
from queue import Queue
from time import sleep, time
from traceback import extract_stack, format_list
from .prop import propertx
from .log import Logger
__all__ = [
 'ThreadPool', 'Worker']
__docformat__ = 'restructuredtext'

class ThreadPool(Logger):
    """"""
    NoJob = 6 * (None, )

    def __init__(self, name=None, parent=None, Psize=20, Qsize=20, daemons=True):
        Logger.__init__(self, name, parent)
        self._daemons = daemons
        self.localThreadId = 0
        self.workers = []
        self.jobs = Queue(Qsize)
        self.size = Psize
        self.accept = True

    @propertx
    def size():

        def set(self, newSize):
            """set method for the size property"""
            nb_workers = len(self.workers)
            if newSize == nb_workers:
                return
            for i in range(newSize - nb_workers):
                self.localThreadId += 1
                name = '%s.W%03i' % (self.log_name, self.localThreadId)
                new = Worker(self, name, self._daemons)
                self.workers.append(new)
                self.debug('Starting %s' % name)
                new.start()

            nb_workers = len(self.workers)
            for i in range(nb_workers - newSize):
                self.jobs.put(self.NoJob)

        def get(self):
            """get method for the size property"""
            return len(self.workers)

        return (
         get, set, None, 'number of threads')

    def add(self, job, callback=None, *args, **kw):
        if self.accept:
            th_id, stack = currentThread().name, extract_stack()[:-1]
            self.jobs.put((job, args, kw, callback, th_id, stack))

    def join(self):
        self.accept = False
        while True:
            for w in self.workers:
                if w.isAlive():
                    self.jobs.put(self.NoJob)
                    break
            else:
                break

    @property
    def qsize(self):
        return self.jobs.qsize()

    def getNumOfBusyWorkers(self):
        """ Get the number of workers that are in busy mode.
        """
        n = 0
        for w in self.workers:
            if w.isBusy():
                n += 1

        return n


class Worker(Thread, Logger):

    def __init__(self, pool, name=None, daemon=True):
        name = name or self.__class__.__name__
        Thread.__init__(self, name=name)
        Logger.__init__(self, name, pool)
        self.daemon = daemon
        self.pool = pool
        self.cmd = ''
        self.busy = False

    def run(self):
        get = self.pool.jobs.get
        while True:
            cmd, args, kw, callback, th_id, stack = get()
            if cmd:
                self.busy = True
                self.cmd = cmd.__name__
                try:
                    try:
                        if callback:
                            callback(cmd(*args, **kw))
                        else:
                            cmd(*args, **kw)
                    except:
                        orig_stack = ('').join(format_list(stack))
                        self.error("Uncaught exception running job '%s' called from thread %s:\n%s", self.cmd, th_id, orig_stack, exc_info=1)

                finally:
                    self.busy = False
                    self.cmd = ''

            else:
                self.pool.workers.remove(self)
                return

    def isBusy(self):
        return self.busy


if __name__ == '__main__':

    def easyJob(*arg, **kw):
        n = arg[0]
        print('\tSleep\t\t', n)
        sleep(n)
        return 'Slept\t%d' % n


    def longJob(*arg, **kw):
        print('\tStart\t\t\t', arg, kw)
        n = arg[0] * 3
        sleep(n)
        return 'Job done in %d' % n


    def badJob(*a, **k):
        print('\n !!! OOOPS !!!\n')
        a = 1 / 0


    def show(*arg, **kw):
        print('callback : %s' % arg[0])


    def test_1(**kwargs):
        workers = kwargs.pop('workers', 5)
        jobqueue = kwargs.pop('jobqueue', 10)
        pool = ThreadPool(name='ThreadPool', Psize=workers, Qsize=jobqueue)
        print("\n\t\t... let's add some jobs ...\n")
        for j in range(5):
            if j == 1:
                pool.add(badJob)
            for i in range(5, 0, -1):
                pool.add(longJob, show, i)
                pool.add(easyJob, show, i)

        print("\n            \t\t... and now, we're waiting for the %i workers to get the %i jobs done ...\n        " % (pool.size, pool.qsize))
        sleep(15)
        print("\n\t\t... ok, that may take a while, let's get some reinforcement ...\n")
        sleep(5)
        pool.size = 50
        print('\n\t\t... Joining ...\n')
        pool.join()
        print('\n\t\t... Ok ...\n')


    def test_2(**kwargs):
        workers = kwargs.pop('workers', 5)
        jobqueue = kwargs.pop('jobqueue', 10)
        numjobs = kwargs.pop('numjobs', 10)
        sleep_t = kwargs.pop('sleep_t', 1)
        pool = ThreadPool(name='ThreadPool', Psize=workers, Qsize=jobqueue)
        print('\n\t\t... Check the number of busy workers ...\n')
        print('Num of busy workers = %s' % pool.getNumOfBusyWorkers())
        print("\n\t\t... let's add some jobs ...\n")
        for i in range(numjobs):
            pool.add(easyJob, None, sleep_t)

        print('\n\t\t... Monitoring the busy workers ...\n')
        t0 = time()
        while pool.getNumOfBusyWorkers() > 0:
            print('busy workers = %s' % pool.getNumOfBusyWorkers())
            sleep(0.5)

        t1 = time()
        print('Run %s jobs of 1 second took %.3f' % (numjobs, t1 - t0))
        print('\n\t\t... Joining ...\n')
        pool.join()
        print('\n\t\t... Ok ...\n')
        return


    def main(argv):
        kwargs = {}
        for arg in argv:
            k, v = arg.split('=')
            kwargs[k] = int(v)

        test_1(**kwargs)
        test_2(**kwargs)


    import sys
    main(sys.argv[1:])