# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/taskqueue/tasks.py
# Compiled at: 2007-07-24 13:08:31
"""
Task management for the task queue workers
"""
from twisted.internet import defer, reactor
from workers import IWorker
from errors import ImplementationError

class Task(object):
    """
    I represent a task that has been dispatched to a queue for running with a
    given scheduling I{niceness}. I generate a C{Deferred}, accessible as an
    attribute I{d}, firing it when the task is finally run and its result is
    obtained.
    
    @ivar d: A deferred to the eventual result of the task.
    
    @ivar series: A hashable object identifying the series of which this task
      is a part.

    """
    __module__ = __name__

    def __init__(self, f, args, kw, priority, series):
        if not isinstance(args, (tuple, list)):
            raise TypeError("Second argument 'args' isn't a sequence")
        if not isinstance(kw, dict):
            raise TypeError("Third argument 'kw' isn't a dict")
        self.callTuple = (
         f, args, kw)
        self.priority = priority
        self.series = series
        self.d = defer.Deferred()

    def __repr__(self):
        """
        Gives me an informative string representation
        """
        func = self.callTuple[0]
        args = (', ').join([ str(x) for x in self.callTuple[1] ])
        kw = ('').join([ ', %s=%s' % item for item in self.callTuple[2].iteritems() ])
        if func.__class__.__name__ == 'function':
            funcName = func.__name__
        elif callable(func):
            funcName = '%s.%s' % (func.__class__.__name__, func.__name__)
        else:
            funcName = '<worker call> '
            args = '%s, ' % func + args
        return 'Task: %s(%s%s)' % (funcName, args, kw)

    def __cmp__(self, other):
        """
        Numeric comparisons between tasks are based on their priority, with
        higher (lower-numbered) priorities being considered "less" and thus
        sorted first.

        A task will always have a higher priority, i.e., be comparatively
        I{less}, than a C{None} object, which is used as a shutdown signal
        instead of a task.
        """
        if other is None:
            return -1
        return cmp(self.priority, other.priority)


class TaskFactory(object):
    """
    I generate L{Task} instances with the right priority setting for effective
    scheduling between tasks in one or more concurrently running task series.
    """
    __module__ = __name__

    def __init__(self, TaskClass=Task):
        self.TaskClass = TaskClass
        self.seriesNumbers = {}

    def new(self, func, args, kw, niceness, series=None):
        """
        Call this to obtain a L{Task} instance that will run in the specified
        I{series} at a priority reflecting the specified I{niceness}.

        The equation for priority has been empirically determined as follows::

            p = k * (1 + nn**2)

        where C{k} is an iterator that increments for each new task and C{nn}
        is niceness normalized from -20...+20 to the range 0...2.
        
        @param func: A callable object to run as the task, the result of which
          will be sent to the callback for the deferred of the task returned by
          this method when it fires.

        @param args: A tuple containing any arguments to include in the call.

        @param kw: A dict containing any keywords to include in the call.
        
        """
        if not isinstance(niceness, int) or abs(niceness) > 20:
            raise ValueError('Niceness must be an integer between -20 and +20')
        positivized = niceness + 20
        priority = self._serial(series) * (1 + (float(positivized) / 10) ** 2)
        return self.TaskClass(func, args, kw, priority, series)

    def _serial(self, series):
        """
        Maintains serial numbers for tasks in one or more separate series, such
        that the numbers in each series increment independently except that any
        new series starts at a value greater than the maximum serial number
        currently found in any series.
        """
        if series not in self.seriesNumbers:
            eachSeries = [
             0] + self.seriesNumbers.values()
            maxCurrentSN = max(eachSeries)
            self.seriesNumbers[series] = maxCurrentSN
        self.seriesNumbers[series] += 1
        return float(self.seriesNumbers[series])


class Assignment(object):
    """
    I represent the assignment of a single task to whichever worker object
    accepts me. Deep down, my real role is to provide something to fire the
    callback of a deferred with instead of just another deferred.
    
    @ivar d: A deferred that is instantiated for a given instance of me, which
      fires when a worker accepts the assigment represented by that instance.

    """
    __module__ = __name__
    __slots__ = [
     'task', 'd']

    def __init__(self, task):
        self.task = task
        self.d = defer.Deferred()

    def accept(self, worker):
        """
        Called when the worker accepts the assignment, firing my
        deferred.
        
        @return: Another deferred that fires when the worker is ready to accept
          B{another} assignment following this one.

        """
        self.d.callback(None)
        return worker.run(self.task)


class AssignmentFactory(object):
    """
    I generate L{Assignment} instances for workers to handle particular tasks.
    """
    __module__ = __name__

    def __init__(self):
        self.waiting = {}
        self.pending = {}

    def cancelRequests(self, worker):
        """
        """
        for (series, dList) in getattr(worker, 'assignments', {}).iteritems():
            requestsWaiting = self.waiting.get(series, [])
            for d in dList:
                if d in requestsWaiting:
                    requestsWaiting.remove(d)

    def request(self, worker, series):
        """
        Called to request a new assignment in the specified I{series} of tasks
        for the supplied I{worker}.

        When a new assignment in the series is finally ready in the queue for
        this worker, the deferred for the assignment request will fire with an
        instance of me that has been constructed with the task to be assigned.

        If the worker is still gainfully employed when it accepts the
        assignment, and is not just wrapping up its work after having been
        fired, the worker will request another assignment when it finishes the
        task.
        """

        def accept(assignment, d_request):
            worker.assignments[series].remove(d_request)
            if isinstance(assignment, Assignment):
                d = assignment.accept(worker)
                if worker.hired:
                    d.addCallback(lambda _: self.request(worker, series))
                return d

        assignments = getattr(worker, 'assignments', {})
        if self.pending.get(series, []):
            d = defer.succeed(self.pending[series].pop(0))
        else:
            d = defer.Deferred()
            self.waiting.setdefault(series, []).append(d)
        assignments.setdefault(series, []).append(d)
        worker.assignments = assignments
        d.addCallback(accept, d)

    def new(self, task):
        """
        Creates and queues a new assignment for the supplied I{task}, returning
        a deferred that fires when the assignment has been accepted.
        """
        series = task.series
        assignment = Assignment(task)
        if self.waiting.get(series, []):
            self.waiting[series].pop(0).callback(assignment)
        else:
            self.pending.setdefault(series, []).append(assignment)
        return assignment.d


class WorkerManager(object):
    """
    I manage one or more providers of L{IWorker} for a particular instance of
    L{TaskQueue}.

    When a new worker is hired with my L{hire} method, I run the
    L{Assignment.request} class method to request that the worker be assigned a
    task from the queue of each task series for which it is qualified.

    When the worker finally gets the assignment, it fires the L{Assignment}
    object's internal deferred with a reference to itself. That is my cue to
    have the worker run the assigned task and request another assignment of a
    task in the same series when it's done, unless I've terminated the worker
    in the meantime.

    Each worker object maintains a dictionary of deferreds for each of its
    outstanding assignment requests so that I can cancel them if I terminate
    the worker. Then I can effectively cancel the assignment requests by firing
    the deferreds with fake, no-task assignments. See my L{terminate} method.
    
    @ivar workers: A C{dict} of worker objects that are currently employed by
      me, keyed by a unique integer ID code for each worker.

    """
    __module__ = __name__

    def __init__(self):
        self.workers = {}
        self.assignmentFactory = AssignmentFactory()

    def shutdown(self, timeout=None):
        """
        Shutdown all my workers, then fire them, in turn. Returns a
        deferred that fires when my entire work force has been
        terminated. The deferred result is a list of all tasks, if
        any, that were left unfinished by the work force.
        """

        def gotResults(results):
            unfinishedTasks = []
            for result in results:
                unfinishedTasks.extend(result)

            return unfinishedTasks

        dList = []
        for workerID in self.workers.keys():
            d = self.terminate(workerID, timeout=timeout)
            dList.append(d)

        return defer.gatherResults(dList).addCallback(gotResults)

    def hire(self, worker):
        """
        Adds a new worker to my work force.

        Makes sure that there is an assignment request queue for each task
        series for which the worker is qualified, then has the new worker
        request an initial assignment from each queue.

        @return: An integer ID uniquely identifying the worker.
        
        """
        if not IWorker.providedBy(worker):
            raise ImplementationError("'%s' doesn't provide the IWorker interface" % worker)
        IWorker.validateInvariants(worker)
        worker.hired = True
        worker.assignments = {}
        qualifications = [None] + getattr(worker, 'cQualified', []) + getattr(worker, 'iQualified', [])
        for series in qualifications:
            self.assignmentFactory.request(worker, series)

        workerID = getattr(self, '_workerCounter', 0) + 1
        self._workerCounter = workerID
        self.workers[workerID] = worker
        return workerID

    def terminate(self, workerID, timeout=None, crash=False):
        """
        Removes a worker from my work force, canceling all of its unfullfilled
        assignment requests back from the queue and then attempting to shut it
        down gracefully via its C{stop} method.

        The I{timeout} keyword can be set to a number of seconds after which
        the worker will be terminated rudely via its C{crash} method if it
        hasn't shut down gracefully by then. If the I{crash} keyword is set
        C{True}, the worker is crashed right away without waiting for it to run
        through its pending tasks.

        @return: A deferred that fires when the worker has been removed,
          gracefully or not, with a list of the worker's unfinished tasks.
        
        """

        def crashTheWorker(worker, d):
            unfinished = worker.crash()
            d.callback(unfinished)

        def stopped(result):
            if callID.active():
                callID.cancel()
                return []
            return result

        worker = self.workers.pop(workerID, None)
        if worker is None:
            return defer.succeed([])
        worker.hired = False
        self.assignmentFactory.cancelRequests(worker)
        if crash:
            return defer.succeed(worker.crash())
        d = worker.stop()
        if timeout:
            callID = reactor.callLater(timeout, crashTheWorker, worker, d)
            d.addCallback(stopped)
        else:
            d.addCallback(lambda _: [])
        return d

    def assignment(self, task):
        """
        Generates a new assignment for the supplied I{task}.

        If the worker that runs the task is still working for me when it
        becomes ready for another task following this one, an assignment
        request will be entered for it to obtain another task of the same
        series.
        
        @return: A deferred that fires when the task has been assigned to a
          worker and it has accepted the assignment.

        """
        return self.assignmentFactory.new(task)