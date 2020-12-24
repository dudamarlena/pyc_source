# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/common/threads.py
# Compiled at: 2011-10-12 12:56:51
"""
Thread management

This module provides an abstraction over the threading package, including
the ability to manage the execution of a tree of threads.
"""
import os, sys, signal, threading, traceback
from globus.provision.common import log

class ThreadAbortException(Exception):
    pass


class GPThread(threading.Thread):

    def __init__(self, multi, name, depends=None):
        threading.Thread.__init__(self)
        self.multi = multi
        self.name = name
        self.exception = None
        self.stack_trace = None
        self.status = -1
        self.depends = depends
        return

    def check_continue(self):
        if self.multi.abort.is_set():
            raise ThreadAbortException()

    def run2(self):
        pass

    def run(self):
        try:
            self.run2()
            self.status = 0
        except Exception:
            (exc_type, exc_value, exc_traceback) = sys.exc_info()
            self.exception = exc_value
            self.stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            self.status = 1
            self.multi.thread_failure(self)

        if self.status == 0:
            self.multi.thread_success(self)


class MultiThread(object):

    def __init__(self):
        self.num_threads = 0
        self.done_threads = 0
        self.threads = {}
        self.lock = threading.Lock()
        self.all_done = threading.Event()
        self.abort = threading.Event()

    def add_thread(self, thread):
        self.threads[thread.name] = thread
        self.num_threads += 1

    def run(self):
        self.done_threads = 0
        for t in [ th for th in self.threads.values() if len(th.depends) == 0 ]:
            t.start()

        self.all_done.wait()

    def thread_success(self, thread):
        with self.lock:
            self.done_threads += 1
            log.debug('%s thread has finished successfully.' % thread.name)
            log.debug('%i threads are done. Remaining: %s' % (self.done_threads, (',').join([ t.name for t in self.threads.values() if t.status == -1 ])))
            dependents = [ th for th in self.threads.values() if thread in th.depends ]
            for t in dependents:
                if set(t.depends) <= set([ th for th in self.threads.values() if th.status == 0 ]):
                    t.start()

            if self.done_threads == self.num_threads:
                self.all_done.set()

    def thread_failure(self, thread):
        with self.lock:
            if not isinstance(thread.exception, ThreadAbortException):
                log.debug('%s thread has failed: %s' % (thread.name, thread.exception))
                self.abort.set()
            else:
                log.debug('%s thread is being aborted.' % thread.name)
                thread.status = 2
            self.done_threads += 1
            self.abort_dependents(thread)
            log.debug('%i threads are done. Remaining: %s' % (self.done_threads, (',').join([ t.name for t in self.threads.values() if t.status == -1 ])))
            if self.done_threads == self.num_threads:
                self.all_done.set()

    def abort_dependents(self, thread):
        dep = [ th for th in self.threads.values() if thread in th.depends if th.status != 3 ]
        for th in dep:
            log.debug('%s thread is being aborted because it depends on failed %s thread.' % (th.name, thread.name))
            th.status = 3
            self.done_threads += 1
            self.abort_dependents(th)

    def all_success(self):
        return all([ t.status == 0 for t in self.threads.values() ])

    def get_exceptions(self):
        return dict([ (t.name, (t.exception, t.stack_trace)) for t in self.threads.values() if t.status == 1 ])


class SIGINTWatcher(object):
    """this class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and the process that contains the
    threads.  See Appendix A of The Little Book of Semaphores.
    http://greenteapress.com/semaphores/

    I have only tested this on Linux.  I would expect it to
    work on the Macintosh and not work on Windows.
    """

    def __init__(self, cleanup_func):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.cleanup_func = cleanup_func
        self.child = os.fork()
        if self.child == 0:
            return
        self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.cleanup_func()
            self.kill()

        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass