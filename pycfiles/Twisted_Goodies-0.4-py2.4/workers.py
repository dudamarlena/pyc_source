# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/taskqueue/workers.py
# Compiled at: 2007-07-24 13:08:31
"""
The worker interface and some implementors.
"""
from zope.interface import implements, invariant, Interface, Attribute
from twisted.python import failure
from twisted.internet import defer, reactor
import errors

class IWorker(Interface):
    """
    Provided by worker objects that can have tasks assigned to them for
    processing.

    All worker objects are considered qualified to run tasks of the default
    C{None} series. To indicate that subclasses or subclass instances are
    qualified to run tasks of user-defined series in addition to the default,
    the hashable object that identifies the additional series must be listed in
    the C{cQualified} or C{iQualified} class or instance attributes,
    respectively.
        
    """
    __module__ = __name__
    cQualified = Attribute('\n        A class-attribute list containing all series for which all instances of\n        the subclass are qualified to run tasks.\n        ')
    iQualified = Attribute('\n        An instance-attribute list containing all series for which the subclass\n        instance is qualified to run tasks.\n        ')

    def _check_qualifications(ob):
        """
        Qualification attributes must be present as lists.
        """
        for attrName in ('cQualified', 'iQualified'):
            x = getattr(ob, attrName, None)
            if not isinstance(x, list):
                raise errors.InvariantError(ob)

        return

    invariant(_check_qualifications)

    def setResignator(callableObject):
        """
        Registers the supplied I{callableObject} to be called if the
        worker deems it necessary to resign, e.g., a remote connection
        has been lost.
        """
        pass

    def run(task):
        """
        Adds the task represented by the specified I{task} object to the list
        of tasks pending for this worker, to be run however and whenever the
        worker sees fit.

        Make sure that any callbacks you add to the task's internal deferred
        object C{task.d} return the callback argument. Otherwise, the result of
        your task will be lost in the callback chain.
        
        @return: A deferred that fires when the worker is ready to be assigned
          another task.

        """
        pass

    def stop():
        """
        Attempts to gracefully shut down the worker, returning a deferred that
        fires when the worker is done with all assigned tasks and will not
        cause any errors if the reactor is stopped or its object is deleted.

        The deferred returned by your implementation of this method must not
        fire until B{after} the results of all pending tasks have been
        obtained. Thus the deferred must be chained to each C{task.d} somehow.

        Make sure that any callbacks you add to the task's internal deferred
        object C{task.d} return the callback argument. Otherwise, the result of
        your task will be lost in the callback chain.
        """
        pass

    def crash():
        """
        Takes drastic action to shut down the worker, rudely and
        synchronously.

        @return: A list of I{task} objects, one for each task left
          uncompleted. You shouldn't have to call this method if no
          tasks are left pending; the L{shutdown} method should be
          enough in that case.
        
        """
        pass


class ThreadWorker:
    """
    I implement an L{IWorker} that runs tasks in a dedicated worker thread.
    """
    __module__ = __name__
    implements(IWorker)
    cQualified = []

    def __init__(self):
        import threading
        self.iQualified = []
        self.event = threading.Event()
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def _loop(self):
        """
        Runs a loop in a dedicated thread that waits for new tasks. The loop
        exits when a C{None} object is supplied as a task.
        """
        while True:
            self.event.wait()
            task = self.task
            if task is None:
                break
            self.event.clear()
            reactor.callFromThread(self.d.callback, None)
            (f, args, kw) = task.callTuple
            try:
                result = f(*args, **kw)
            except Exception, e:
                reactor.callFromThread(task.d.errback, failure.Failure(e))
            else:
                reactor.callFromThread(task.d.callback, result)

        reactor.callFromThread(self.d.callback, None)
        return

    def setResignator(self, callableObject):
        """
        There's nothing that would make me resign.
        """
        pass

    def run(self, task):
        """
        Starts a thread for this worker if one not started already, along with
        a L{threading.Event} object for cross-thread signaling.
        """
        if hasattr(self, 'd') and not self.d.called:
            raise errors.ImplementationError('Task Loop not ready to deal with a task now')
        self.d = defer.Deferred()
        self.task = task
        self.event.set()
        return self.d

    def stop(self):
        """
        The returned deferred fires when the task loop has ended and its thread
        terminated.
        """

        def joinIfPossible(null):
            if hasattr(self, 'task'):
                self.thread.join()

        if hasattr(self, 'task') and self.task is None:
            d = defer.succeed(None)
        else:
            d = defer.Deferred()
            if hasattr(self, 'd') and not self.d.called:
                d.addCallback(lambda _: self.stop())
                self.d.chainDeferred(d)
            else:
                d.addCallback(joinIfPossible)
                self.d = d
                self.task = None
                self.event.set()
        return d

    def crash(self):
        """
        Unfortunately, a thread can only terminate itself, so calling
        this method only forces firing of the deferred returned from a
        previous call to L{stop} and returns the task that hung the
        thread.
        """
        if self.task is not None and not self.task.d.called:
            result = [
             self.task]
        else:
            result = []
        if hasattr(self, 'd') and not self.d.called:
            del self.task
            self.d.callback(None)
        return


class RemoteCallWorker:
    """
    Instances of me provide an L{IWorker} that dispatches
    C{callRemote} tasks, no more than I{N} at a time, to a particular
    I{remoteReference} to a referenceable at a connected PB server.
    """
    __module__ = __name__
    implements(IWorker)
    cQualified = []

    def __init__(self, remoteReference, N=3, noTypeCheck=False):
        from twisted.spread import pb
        if not noTypeCheck:
            if not isinstance(remoteReference, pb.RemoteReference):
                raise TypeError('You must construct me with a PB RemoteReference')
        self.resignators = []
        self.disconnectErrors = (pb.DeadReferenceError, pb.PBConnectionLost)
        remoteReference.notifyOnDisconnect(self._resign)
        self.N = N
        self.iQualified = []
        self.remoteCaller = remoteReference.callRemote
        self.jobs = []
        self.runRequestQueue = defer.DeferredQueue()
        for k in xrange(self.N):
            self.runRequestQueue.put(None)

        return

    def _runNow(self, null, task):
        (suffix, args, kw) = task.callTuple
        d = self.remoteCaller(suffix, *args, **kw)
        job = (task, d)
        self.jobs.append(job)
        d.addCallback(self._doneTrying, job)
        d.addErrback(self._oops)

    def _oops(self, failure):
        if failure.check(*self.disconnectErrors):
            self._resign()
        else:
            return failure

    def _doneTrying(self, result, job):
        self.jobs.remove(job)
        self.runRequestQueue.put(None)
        task = job[0]
        task.d.callback(result)
        return

    def _resign(self, *null):
        while self.resignators:
            callableObject = self.resignators.pop()
            callableObject()

    def setResignator(self, callableObject):
        """
        I will resign upon having one of my tasks turn up a connection
        fault.
        """
        self.resignators.append(callableObject)

    def run(self, task):
        """
        Runs the specified task, which must be a string specifying the suffix
        portion of a method of the referenceable, e.g., I{'foo'} for
        C{remote_foo} or C{perspective_foo}.

        Returns a deferred that fires when one of the pending tasks is done
        running and I can accept another one.
        """
        if getattr(self, 'isShuttingDown', False):
            raise errors.QueueRunError
        return self.runRequestQueue.get().addCallback(self._runNow, task)

    def stop(self):
        """
        The returned deferred fires when all pending tasks are done.
        """
        self.isShuttingDown = True
        return defer.DeferredList([ job[1] for job in self.jobs ])

    def crash(self):
        """
        Return all tasks not completed by the (disconnected) PB server.
        """
        return [ job[0] for job in self.jobs ]


class RemoteInterfaceWorker(RemoteCallWorker):
    """
    Construct an instance of me with a I{remoteReference} and one or more
    interfaces it provides, as arguments.
    """
    __module__ = __name__

    def __init__(self, remoteReference, *interfaces, **kw):
        subseries = kw.get('subseries', None)
        N = kw.get('N', 3)
        RemoteCallWorker.__init__(self, remoteReference, N)
        self.interfaces = interfaces
        for interface in interfaces:
            qualification = interface.__name__
            if subseries:
                qualification += ':%s' % subseries
            self.iQualified.append(qualification)

        self.suffixCache = []
        return

    def _names(self, items):
        nameListing = [ x.__name__ for x in items ]
        nameListing[-1] = 'or ' + nameListing[(-1)]
        joinString = (' ', ', ')[(len(nameListing) > 2)]
        return joinString.join(nameListing)

    def _checkSuffix(self, suffix):
        for interface in self.interfaces:
            for attrName in interface:
                if attrName.endswith('_' + suffix):
                    self.suffixCache.append(suffix)
                    return

        names = self._names(self.interfaces)
        raise AttributeError('No remote method *_%s provided by interface %s' % (suffix, names))

    def _runNow(self, null, task):
        (suffix, args, kw) = task.callTuple
        if suffix not in self.suffixCache:
            self._checkSuffix(suffix)
        d = self.remoteCaller(suffix, *args, **kw)
        job = (task, d)
        self.jobs.append(job)
        d.addBoth(self._doneTrying, job)