# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/xsser/XSSer/threadpool.py
# Compiled at: 2013-12-09 06:41:17
"""
$Id$

This file is part of the xsser project, http://xsser.sourceforge.net.

Copyright (c) 2011/2012 psy <root@lordepsylon.net> - <epsylon@riseup.net>

xsser is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

xsser is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with xsser; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
__docformat__ = 'restructuredtext en'
__all__ = [
 'makeRequests',
 'NoResultsPending',
 'NoWorkersAvailable',
 'ThreadPool',
 'WorkRequest',
 'WorkerThread']
__author__ = 'Christopher Arndt'
__version__ = '1.2.7'
__revision__ = '$Revision: 416 $'
__date__ = '$Date: 2009-10-07 05:41:27 +0200 (Wed, 07 Oct 2009) $'
__license__ = 'MIT license'
import sys, threading
try:
    import Queue
except ImportError:
    import queue as Queue

from Queue import Empty
import traceback

class NoResultsPending(Exception):
    """All work requests have been processed."""
    pass


class NoWorkersAvailable(Exception):
    """No worker threads available to process remaining requests."""
    pass


def _handle_thread_exception(request, exc_info):
    """Default exception handler callback function.

    This just prints the exception info via ``traceback.print_exception``.

    """
    traceback.print_exception(*exc_info)


def makeRequests(callable_, args_list, callback=None, exc_callback=_handle_thread_exception):
    """Create several work requests for same callable with different arguments.

    Convenience function for creating several work requests for the same
    callable where each invocation of the callable receives different values
    for its arguments.

    ``args_list`` contains the parameters for each invocation of callable.
    Each item in ``args_list`` should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    See docstring for ``WorkRequest`` for info on ``callback`` and
    ``exc_callback``.

    """
    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(WorkRequest(callable_, item[0], item[1], callback=callback, exc_callback=exc_callback))
        else:
            requests.append(WorkRequest(callable_, [item], None, callback=callback, exc_callback=exc_callback))

    return requests


class WorkerThread(threading.Thread):
    """Background thread connected to the requests/results queues.

    A worker thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.

    """

    def __init__(self, requests_queue, results_queue, poll_timeout=5, **kwds):
        """Set up thread in daemonic mode and start it immediatedly.

        ``requests_queue`` and ``results_queue`` are instances of
        ``Queue.Queue`` passed by the ``ThreadPool`` class when it creates a new
        worker thread.

        """
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self._requests_queue = requests_queue
        self._results_queue = results_queue
        self._poll_timeout = poll_timeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """Repeatedly process the job queue until told to exit."""
        while True:
            if self._dismissed.isSet():
                break
            try:
                request = self._requests_queue.get(True, self._poll_timeout)
            except Empty:
                continue
            else:
                if self._dismissed.isSet():
                    self._requests_queue.put(request)
                    break
                try:
                    result = request.callable(*request.args, **request.kwds)
                    self._results_queue.put((request, result))
                except:
                    request.exception = True
                    self._results_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """Sets a flag to tell the thread to exit when done with current job."""
        self._dismissed.set()


class WorkRequest:
    """A request to execute a callable for putting in the request queue later.

    See the module function ``makeRequests`` for the common case
    where you want to build several ``WorkRequest`` objects for the same
    callable but with different arguments for each call.

    """

    def __init__(self, callable_, args=None, kwds=None, requestID=None, callback=None, exc_callback=_handle_thread_exception):
        """Create a work request for a callable and attach callbacks.

        A work request consists of the a callable to be executed by a
        worker thread, a list of positional arguments, a dictionary
        of keyword arguments.

        A ``callback`` function can be specified, that is called when the
        results of the request are picked up from the result queue. It must
        accept two anonymous arguments, the ``WorkRequest`` object and the
        results of the callable, in that order. If you want to pass additional
        information to the callback, just stick it on the request object.

        You can also give custom callback for when an exception occurs with
        the ``exc_callback`` keyword parameter. It should also accept two
        anonymous arguments, the ``WorkRequest`` and a tuple with the exception
        details as returned by ``sys.exc_info()``. The default implementation
        of this callback just prints the exception info via
        ``traceback.print_exception``. If you want no exception handler
        callback, just pass in ``None``.

        ``requestID``, if given, must be hashable since it is used by
        ``ThreadPool`` object to store the results of that work request in a
        dictionary. It defaults to the return value of ``id(self)``.

        """
        if requestID is None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError('requestID must be hashable.')

        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}
        return

    def __str__(self):
        return '<WorkRequest id=%s args=%r kwargs=%r exception=%s>' % (
         self.requestID, self.args, self.kwds, self.exception)


class ThreadPool:
    """A thread pool, distributing work requests and collecting results.

    See the module docstring for more information.

    """

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        """Set up the thread pool and start num_workers worker threads.

        ``num_workers`` is the number of worker threads to start initially.

        If ``q_size > 0`` the size of the work *request queue* is limited and
        the thread pool blocks when the queue is full and it tries to put
        more work requests in it (see ``putRequest`` method), unless you also
        use a positive ``timeout`` value for ``putRequest``.

        If ``resq_size > 0`` the size of the *results queue* is limited and the
        worker threads will block when the queue is full and they try to put
        new results in it.

        .. warning:
            If you set both ``q_size`` and ``resq_size`` to ``!= 0`` there is
            the possibilty of a deadlock, when the results queue is not pulled
            regularly and too many jobs are put in the work requests queue.
            To prevent this, always set ``timeout > 0`` when calling
            ``ThreadPool.putRequest()`` and catch ``Queue.Full`` exceptions.

        """
        self._requests_queue = Queue.Queue(q_size)
        self._results_queue = Queue.Queue(resq_size)
        self.workers = []
        self.dismissedWorkers = []
        self.workRequests = {}
        self.createWorkers(num_workers, poll_timeout)

    def createWorkers(self, num_workers, poll_timeout=5):
        """Add num_workers worker threads to the pool.

        ``poll_timout`` sets the interval in seconds (int or float) for how
        ofte threads should check whether they are dismissed, while waiting for
        requests.

        """
        for i in range(num_workers):
            self.workers.append(WorkerThread(self._requests_queue, self._results_queue, poll_timeout=poll_timeout))

    def dismissWorkers(self, num_workers, do_join=False):
        """Tell num_workers worker threads to quit after their current task."""
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)

        if do_join:
            for worker in dismiss_list:
                worker.join()

        else:
            self.dismissedWorkers.extend(dismiss_list)

    def joinAllDismissedWorkers(self):
        """Perform Thread.join() on all worker threads that have been dismissed.
        """
        for worker in self.dismissedWorkers:
            worker.join()

        self.dismissedWorkers = []

    def putRequest(self, request, block=True, timeout=None):
        """Put work request into work queue and save its id for later."""
        assert isinstance(request, WorkRequest)
        assert not getattr(request, 'exception', None)
        self._requests_queue.put(request, block, timeout)
        self.workRequests[request.requestID] = request
        return

    def addRequest(self, do_cb, data, print_cb, exception_cb, block=True, timeout=None):
        """Put work request into work queue and save its id for later."""
        requests = makeRequests(do_cb, data, print_cb, exception_cb)
        for req in requests:
            self.putRequest(req, block, timeout)

    def poll(self, block=False):
        """Process any new results in the queue."""
        while True:
            if not self.workRequests:
                raise NoResultsPending
            else:
                if block and not self.workers:
                    raise NoWorkersAvailable
                try:
                    request, result = self._results_queue.get(block=block)
                    if request.exception and request.exc_callback:
                        request.exc_callback(request, result)
                    if request.callback and not (request.exception and request.exc_callback):
                        request.callback(request, result)
                    del self.workRequests[request.requestID]
                except Empty:
                    break

    def wait(self):
        """Wait for results, blocking until all have arrived."""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break


if __name__ == '__main__':
    import random, time

    def do_something(data):
        time.sleep(random.randint(1, 5))
        result = round(random.random() * data, 5)
        if result > 5:
            raise RuntimeError('Something extraordinary happened!')
        return result


    def print_result(request, result):
        print '**** Result from request #%s: %r' % (request.requestID, result)


    def handle_exception(request, exc_info):
        if not isinstance(exc_info, tuple):
            print request
            print exc_info
            raise SystemExit
        print '**** Exception occured in request #%s: %s' % (
         request.requestID, exc_info)


    data = [ random.randint(1, 10) for i in range(20) ]
    requests = makeRequests(do_something, data, print_result, handle_exception)
    data = [ ((random.randint(1, 10),), {}) for i in range(20) ]
    requests.extend(makeRequests(do_something, data, print_result, handle_exception))
    print 'Creating thread pool with 3 worker threads.'
    main = ThreadPool(3)
    for req in requests:
        main.putRequest(req)
        print 'Work request #%s added.' % req.requestID

    i = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()
            print ('Main thread working...', )
            print '(active worker threads: %i)' % (threading.activeCount() - 1,)
            if i == 10:
                print '**** Adding 3 more worker threads...'
                main.createWorkers(3)
            if i == 20:
                print '**** Dismissing 2 worker threads...'
                main.dismissWorkers(2)
            i += 1
        except KeyboardInterrupt:
            print '**** Interrupted!'
            break
        except NoResultsPending:
            print '**** No pending results.'
            break

    if main.dismissedWorkers:
        print 'Joining all dismissed worker threads...'
        main.joinAllDismissedWorkers()