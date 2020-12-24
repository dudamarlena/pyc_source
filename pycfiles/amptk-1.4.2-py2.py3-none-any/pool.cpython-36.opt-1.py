# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ampoule/pool.py
# Compiled at: 2019-12-22 01:42:51
# Size of source mod 2**32: 15201 bytes
import time, random, heapq, itertools, functools, signal
choice = random.choice
now = time.time
count = functools.partial(next, itertools.count())
pop = heapq.heappop
from twisted import logger
from twisted.internet import defer, task, error
from twisted.python.failure import Failure
from ampoule import commands, main
log = logger.Logger()
STATS_TEMPLATE = 'ProcessPool stats:\n    workers:       {w}\n    timeout:       {t}\n    parent:        {p}\n    child:         {c}\n    max idle:      {i}\n    recycle after: {r}\n    ProcessStarter:\n                   {s}'
try:
    DIE = signal.SIGKILL
except AttributeError:
    DIE = signal.SIGTERM

class ProcessPool(object):
    """ProcessPool"""
    finished = False
    started = False
    name = None

    def __init__(self, ampChild=None, ampParent=None, min=5, max=20, name=None, maxIdle=20, recycleAfter=500, starter=None, timeout=None, timeout_signal=DIE, ampChildArgs=()):
        self.starter = starter
        self.ampChildArgs = tuple(ampChildArgs)
        if starter is None:
            self.starter = main.ProcessStarter(packages=('twisted', ))
        self.ampParent = ampParent
        self.ampChild = ampChild
        if ampChild is None:
            from ampoule.child import AMPChild
            self.ampChild = AMPChild
        self.min = min
        self.max = max
        self.name = name
        self.maxIdle = maxIdle
        self.recycleAfter = recycleAfter
        self.timeout = timeout
        self.timeout_signal = timeout_signal
        self._queue = []
        self.processes = set()
        self.ready = set()
        self.busy = set()
        self._finishCallbacks = {}
        self._lastUsage = {}
        self._calls = {}
        self.looping = task.LoopingCall(self._pruneProcesses)
        self.looping.start(maxIdle, now=False)

    def start(self, ampChild=None):
        """
        Starts the ProcessPool with a given child protocol.

        @param ampChild: a L{ampoule.child.AMPChild} subclass.
        @type ampChild: L{ampoule.child.AMPChild} subclass
        """
        if ampChild is not None:
            if not self.started:
                self.ampChild = ampChild
        self.finished = False
        self.started = True
        return self.adjustPoolSize()

    def _pruneProcesses(self):
        """
        Remove idle processes from the pool.
        """
        n = now()
        d = []
        for child, lastUse in self._lastUsage.items():
            if len(self.processes) > self.min and n - lastUse > self.maxIdle and child not in self.busy:
                self.ready.discard(child)
                self.processes.discard(child)
                d.append(self.stopAWorker(child))

        return defer.DeferredList(d)

    def _pruneProcess(self, child):
        """
        Remove every trace of the process from this instance.
        """
        self.processes.discard(child)
        self.ready.discard(child)
        self.busy.discard(child)
        self._lastUsage.pop(child, None)
        self._calls.pop(child, None)
        self._finishCallbacks.pop(child, None)

    def _addProcess(self, child, finished):
        """
        Adds the newly created child process to the pool.
        """

        def fatal(reason, child):
            log.error('FATAL: Process exited.\n\t{r}',
              r=(reason.getErrorMessage()))
            self._pruneProcess(child)

        def dieGently(data, child):
            log.info('STOPPING: {s}', s=data)
            self._pruneProcess(child)

        self.processes.add(child)
        self.ready.add(child)
        finished.addCallback(dieGently, child).addErrback(fatal, child)
        self._finishCallbacks[child] = finished
        self._lastUsage[child] = now()
        self._calls[child] = 0
        self._catchUp()

    def _catchUp(self):
        """
        If there are queued items in the list then run them.
        """
        if self._queue:
            _, (d, command, kwargs) = pop(self._queue)
            (self._cb_doWork)(command, **kwargs).chainDeferred(d)

    def _handleTimeout(self, child):
        """
        One of the children went timeout, we need to deal with it

        @param child: The child process
        @type child: L{child.AMPChild}
        """
        try:
            child.transport.signalProcess(self.timeout_signal)
        except error.ProcessExitedAlready:
            pass

    def startAWorker(self):
        """
        Start a worker and set it up in the system.
        """
        if self.finished:
            return
        else:
            startAMPProcess = self.starter.startAMPProcess
            child, finished = startAMPProcess((self.ampChild), ampParent=(self.ampParent),
              ampChildArgs=(self.ampChildArgs))
            return self._addProcess(child, finished)

    def _cb_doWork(self, command, _timeout=None, _deadline=None, **kwargs):
        """
        Go and call the command.

        @param command: The L{amp.Command} to be executed in the child
        @type command: L{amp.Command}

        @param _d: The deferred for the calling code.
        @type _d: L{defer.Deferred}

        @param _timeout: The timeout for this call only
        @type _timeout: C{int}
        @param _deadline: The deadline for this call only
        @type _deadline: C{int}
        """
        timeoutCall = None
        deadlineCall = None

        def _returned(result, child, is_error=False):

            def cancelCall(call):
                if call is not None:
                    if call.active():
                        call.cancel()

            cancelCall(timeoutCall)
            cancelCall(deadlineCall)
            self.busy.discard(child)
            alreadyDead = is_error and result.check(error.ProcessTerminated)
            if not (die or alreadyDead):
                self.ready.add(child)
                self._catchUp()
            else:
                self.stopAWorker(child).addCallback(lambda _: self.startAWorker())
            self._lastUsage[child] = now()
            return result

        die = False
        child = self.ready.pop()
        self.busy.add(child)
        self._calls[child] += 1
        if self.recycleAfter:
            if self._calls[child] >= self.recycleAfter:
                die = True
        else:
            if _timeout == 0:
                timeout = _timeout
            else:
                timeout = _timeout or self.timeout
        if timeout is not None:
            from twisted.internet import reactor
            timeoutCall = reactor.callLater(timeout, self._handleTimeout, child)
        if _deadline is not None:
            from twisted.internet import reactor
            delay = max(0, _deadline - reactor.seconds())
            deadlineCall = reactor.callLater(delay, self._handleTimeout, child)
        return (defer.maybeDeferred)((child.callRemote), command, **kwargs).addCallback(_returned, child).addErrback(_returned,
          child, is_error=True)

    def callRemote(self, *args, **kwargs):
        """
        Proxy call to keep the API homogeneous across twisted's RPCs
        """
        return (self.doWork)(*args, **kwargs)

    def doWork(self, command, **kwargs):
        """
        Sends the command to one child.

        @param command: an L{amp.Command} type object.
        @type command: L{amp.Command}

        @param kwargs: dictionary containing the arguments for the command.
        """
        if self.ready:
            return (self._cb_doWork)(command, **kwargs)
        else:
            if len(self.processes) < self.max:
                self.startAWorker()
                return (self._cb_doWork)(command, **kwargs)
            d = defer.Deferred()
            self._queue.append((count(), (d, command, kwargs)))
            return d

    def stopAWorker(self, child=None):
        """
        Gently stop a child so that it's not restarted anymore

        @param child: an L{ampoule.child.AmpChild} type object.
        @type child: L{ampoule.child.AmpChild} or None

        """
        if child is None:
            if self.ready:
                child = self.ready.pop()
            else:
                child = choice(list(self.processes))
        child.callRemote(commands.Shutdown).addErrback(lambda reason: reason.trap(error.ProcessTerminated))
        return self._finishCallbacks[child]

    def adjustPoolSize(self, min=None, max=None):
        """
        Change the pool size to be at least min and less than max,
        useful when you change the values of max and min in the instance
        and you want the pool to adapt to them.
        """
        if min is None:
            min = self.min
        else:
            if max is None:
                max = self.max
            else:
                assert min >= 0, 'minimum is negative'
                assert min <= max, 'minimum is greater than maximum'
            self.min = min
            self.max = max
            l = []
            if self.started:
                for i in range(len(self.processes) - self.max):
                    l.append(self.stopAWorker())

                while len(self.processes) < self.min:
                    self.startAWorker()

        return defer.DeferredList(l).addCallback(lambda _: self.dumpStats())

    def stop(self):
        """
        Stops the process protocol.
        """
        self.finished = True
        l = [self.stopAWorker(process) for process in self.processes]

        def _cb(_):
            if self.looping.running:
                self.looping.stop()

        return defer.DeferredList(l).addCallback(_cb)

    def dumpStats(self):
        log.info(STATS_TEMPLATE,
          w=(len(self.processes)),
          t=(self.timeout),
          p=(self.ampParent),
          c=(self.ampChild),
          i=(self.maxIdle),
          r=(self.recycleAfter),
          s=(self.starter))


pp = None

def deferToAMPProcess(command, **kwargs):
    """
    Helper function that sends a command to the default process pool
    and returns a deferred that fires when the result of the
    subprocess computation is ready.

    @param command: an L{amp.Command} subclass
    @param kwargs: dictionary containing the arguments for the command.

    @return: a L{defer.Deferred} with the data from the subprocess.
    """
    global pp
    if pp is None:
        pp = ProcessPool()
        return pp.start().addCallback(lambda _: (pp.doWork)(command, **kwargs))
    else:
        return (pp.doWork)(command, **kwargs)