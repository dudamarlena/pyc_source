# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/singleMachine.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 27959 bytes
from __future__ import absolute_import
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
from contextlib import contextmanager
import logging, os, time, math, subprocess, sys, traceback
from threading import Thread, Event
from threading import Lock, Condition
from six.moves.queue import Empty, Queue
import toil
from toil.batchSystems.abstractBatchSystem import BatchSystemSupport, EXIT_STATUS_UNAVAILABLE_VALUE, UpdatedBatchJobInfo
from toil.lib.threading import cpu_count
from toil import worker as toil_worker
from toil.common import Toil
log = logging.getLogger(__name__)

class SingleMachineBatchSystem(BatchSystemSupport):
    __doc__ = '\n    The interface for running jobs on a single machine, runs all the jobs you\n    give it as they come in, but in parallel.\n\n    Uses a single "daddy" thread to manage a fleet of child processes.\n    \n    Communication with the daddy thread happens via two queues: one queue of\n    jobs waiting to be run (the input queue), and one queue of jobs that are\n    finished/stopped and need to be returned by getUpdatedBatchJob (the output\n    queue).\n\n    When the batch system is shut down, the daddy thread is stopped.\n\n    If running in debug-worker mode, jobs are run immediately as they are sent\n    to the batch system, in the sending thread, and the daddy thread is not\n    run. But the queues are still used.\n    '

    @classmethod
    def supportsAutoDeployment(cls):
        return False

    @classmethod
    def supportsWorkerCleanup(cls):
        return True

    numCores = cpu_count()
    minCores = 0.1
    physicalMemory = toil.physicalMemory()

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        if maxCores > self.numCores:
            if maxCores != sys.maxsize:
                log.warning('Not enough cores! User limited to %i but we only have %i.', maxCores, self.numCores)
            maxCores = self.numCores
        else:
            if maxMemory > self.physicalMemory:
                if maxMemory != sys.maxsize:
                    log.warning('Not enough memory! User limited to %i bytes but we only have %i bytes.', maxMemory, self.physicalMemory)
                maxMemory = self.physicalMemory
            else:
                self.physicalDisk = toil.physicalDisk(config)
                if maxDisk > self.physicalDisk:
                    if maxDisk != sys.maxsize:
                        log.warning('Not enough disk space! User limited to %i bytes but we only have %i bytes.', maxDisk, self.physicalDisk)
                    maxDisk = self.physicalDisk
                super(SingleMachineBatchSystem, self).__init__(config, maxCores, maxMemory, maxDisk)
                assert self.maxCores >= self.minCores
                assert self.maxMemory >= 1
                self.scale = config.scale
                if config.badWorker > 0:
                    if config.debugWorker:
                        raise RuntimeError('Cannot use badWorker and debugWorker together; worker would have to kill the leader')
            self.debugWorker = config.debugWorker
            self.jobIndex = 0
            self.jobIndexLock = Lock()
            self.jobs = {}
            self.inputQueue = Queue()
            self.outputQueue = Queue()
            self.runningJobs = {}
            self.children = {}
            self.childToJob = {}
            self.coreFractions = ResourcePool(int(old_div(self.maxCores, self.minCores)), 'cores')
            self.memory = ResourcePool(self.maxMemory, 'memory')
            self.disk = ResourcePool(self.maxDisk, 'disk')
            self.shuttingDown = Event()
            self.daddyThread = None
            self.daddyException = None
            if self.debugWorker:
                log.debug('Started in worker debug mode.')
            else:
                self.daddyThread = Thread(target=(self.daddy), daemon=True)
                self.daddyThread.start()
                log.debug('Started in normal mode.')

    def daddy(self):
        """
        Be the "daddy" thread.

        Our job is to look at jobs from the input queue.
        
        If a job fits in the available resources, we allocate resources for it
        and kick off a child process.

        We also check on our children.

        When a child finishes, we reap it, release its resources, and put its
        information in the output queue.
        """
        try:
            log.debug('Started daddy thread.')
            while not self.shuttingDown.is_set():
                while not self.shuttingDown.is_set():
                    try:
                        args = self.inputQueue.get_nowait()
                        jobCommand, jobID, jobCores, jobMemory, jobDisk, environment = args
                        coreFractions = int(old_div(jobCores, self.minCores))
                        result = self._startChild(jobCommand, jobID, coreFractions, jobMemory, jobDisk, environment)
                        log.debug('Tried to start job %s and got: %s', jobID, str(result))
                        if result is None:
                            self.inputQueue.put(args)
                            break
                    except Empty:
                        break

                for done_pid in self._pollForDoneChildrenIn(self.children):
                    self._handleChild(done_pid)

                time.sleep(0.01)

            for popen in self.children.values():
                popen.kill()

            for popen in self.children.values():
                popen.wait()

            return
        except Exception as e:
            log.critical('Unhandled exception in daddy thread: %s', traceback.format_exc())
            self.daddyException = e
            raise

    def _checkOnDaddy(self):
        if self.daddyException is not None:
            log.critical('Propagating unhandled exception in daddy thread to main thread')
            exc = self.daddyException
            self.daddyException = None
            raise exc

    def _pollForDoneChildrenIn(self, pid_to_popen):
        """
        See if any children represented in the given dict from PID to Popen
        object have finished.
        
        Return a collection of their PIDs.
        
        Guarantees that each child's exit code will be gettable via wait() on
        the child's Popen object (i.e. does not reap the child, unless via
        Popen).
        """
        ready = set()
        waitid = getattr(os, 'waitid', None)
        if callable(waitid):
            while True:
                try:
                    siginfo = waitid(os.P_ALL, -1, os.WEXITED | os.WNOWAIT | os.WNOHANG)
                except ChildProcessError:
                    siginfo = None

                if siginfo is not None and siginfo.si_pid in pid_to_popen and siginfo.si_pid not in ready:
                    ready.add(siginfo.si_pid)
                else:
                    return ready

        else:
            for pid, popen in pid_to_popen.items():
                if popen.poll() is not None:
                    ready.add(pid)
                    log.debug('Child %d has stopped', pid)

            return ready

    def _runDebugJob(self, jobCommand, jobID, environment):
        """
        Run the jobCommand right now, in the current thread.
        May only be called in debug-worker mode.
        Assumes resources are available.
        """
        if not self.debugWorker:
            raise AssertionError
        else:
            info = Info((time.time()), None, None, killIntended=False)
            self.runningJobs[jobID] = info
            if jobCommand.startswith('_toil_worker '):
                jobName, jobStoreLocator, jobStoreID = jobCommand.split()[1:]
                jobStore = Toil.resumeJobStore(jobStoreLocator)
                toil_worker.workerScript(jobStore, (jobStore.config), jobName, jobStoreID, redirectOutputToLogFile=(not self.debugWorker))
            else:
                subprocess.check_call(jobCommand, shell=True,
                  env=dict((os.environ), **environment))
        self.runningJobs.pop(jobID)
        if not info.killIntended:
            self.outputQueue.put(UpdatedBatchJobInfo(jobID=jobID, exitStatus=0, wallTime=(time.time() - info.time), exitReason=None))

    def _startChild(self, jobCommand, jobID, coreFractions, jobMemory, jobDisk, environment):
        """
        Start a child process for the given job.
        
        Allocate its required resources and save it and save it in our bookkeeping structures.

        If the job is started, returns its PID.
        If the job fails to start, reports it as failed and returns False.
        If the job cannot get the resources it needs to start, returns None.
        """
        popen = None
        startTime = time.time()
        if self.coreFractions.acquireNow(coreFractions):
            if self.memory.acquireNow(jobMemory):
                if self.disk.acquireNow(jobDisk):
                    try:
                        popen = subprocess.Popen(jobCommand, shell=True,
                          env=dict((os.environ), **environment))
                    except Exception:
                        self.coreFractions.release(coreFractions)
                        self.memory.release(jobMemory)
                        self.disk.release(jobDisk)
                        log.error('Could not start job %s: %s', jobID, traceback.format_exc())
                        self.outputQueue.put(UpdatedBatchJobInfo(jobID=jobID, exitStatus=EXIT_STATUS_UNAVAILABLE_VALUE, wallTime=0, exitReason=None))
                        self.coreFractions.release(coreFractions)
                        self.memory.release(jobMemory)
                        self.disk.release(jobDisk)
                        return False
                    else:
                        self.children[popen.pid] = popen
                        self.childToJob[popen.pid] = jobID
                        info = Info(startTime, popen, (coreFractions, jobMemory, jobDisk), killIntended=False)
                        self.runningJobs[jobID] = info
                        log.debug('Launched job %s as child %d', jobID, popen.pid)
                        assert popen.pid != 0
                        return popen.pid
                else:
                    self.coreFractions.release(coreFractions)
                    self.memory.release(jobMemory)
                    log.debug('Not enough disk to run job %s', jobID)
            else:
                self.coreFractions.release(coreFractions)
                log.debug('Not enough memory to run job %s', jobID)
        else:
            log.debug('Not enough cores to run job %s', jobID)

    def _handleChild(self, pid):
        """
        Handle a child process PID that has finished.
        The PID must be for a child job we started.
        Not thread safe to run at the same time as we are making more children.

        Remove the child from our bookkeeping structures and free its resources.
        """
        popen = self.children[pid]
        jobID = self.childToJob[pid]
        info = self.runningJobs[jobID]
        coreFractions, jobMemory, jobDisk = info.resources
        self.runningJobs.pop(jobID)
        self.childToJob.pop(pid)
        self.children.pop(pid)
        statusCode = popen.wait()
        if statusCode != 0:
            if not info.killIntended:
                log.error('Got exit code %i (indicating failure) from job %s.', statusCode, self.jobs[jobID])
        if not info.killIntended:
            self.outputQueue.put(UpdatedBatchJobInfo(jobID=jobID, exitStatus=statusCode, wallTime=(time.time() - info.time), exitReason=None))
        self.coreFractions.release(coreFractions)
        self.memory.release(jobMemory)
        self.disk.release(jobDisk)
        log.debug('Child %d for job %s succeeded', pid, jobID)

    def issueBatchJob(self, jobNode):
        """Adds the command and resources to a queue to be run."""
        self._checkOnDaddy()
        cores = math.ceil(jobNode.cores * self.scale / self.minCores) * self.minCores
        if not cores <= self.maxCores:
            raise AssertionError('The job {} is requesting {} cores, more than the maximum of {} cores this batch system was configured with. Scale is set to {}.'.format(jobNode.jobName, cores, self.maxCores, self.scale))
        else:
            if not cores >= self.minCores:
                raise AssertionError
            elif not jobNode.memory <= self.maxMemory:
                raise AssertionError('The job {} is requesting {} bytes of memory, more than the maximum of {} this batch system was configured with.'.format(jobNode.jobName, jobNode.memory, self.maxMemory))
            self.checkResourceRequest(jobNode.memory, cores, jobNode.disk)
            log.debug('Issuing the command: %s with memory: %i, cores: %i, disk: %i' % (
             jobNode.command, jobNode.memory, cores, jobNode.disk))
            with self.jobIndexLock:
                jobID = self.jobIndex
                self.jobIndex += 1
            self.jobs[jobID] = jobNode.command
            if self.debugWorker:
                self._runDebugJob(jobNode.command, jobID, self.environment.copy())
            else:
                self.inputQueue.put((jobNode.command, jobID, cores, jobNode.memory,
                 jobNode.disk, self.environment.copy()))
        return jobID

    def killBatchJobs(self, jobIDs):
        """Kills jobs by ID."""
        self._checkOnDaddy()
        log.debug('Killing jobs: {}'.format(jobIDs))
        for jobID in jobIDs:
            if jobID in self.runningJobs:
                info = self.runningJobs[jobID]
                info.killIntended = True
                if info.popen != None:
                    log.debug('Send kill to PID %s', info.popen.pid)
                    info.popen.kill()
                    log.debug('Sent kill to PID %s', info.popen.pid)
                else:
                    assert self.debugWorker
                    log.critical("Can't kill job: %s in debug mode" % jobID)
                while jobID in self.runningJobs:
                    pass

    def getIssuedBatchJobIDs(self):
        """Just returns all the jobs that have been run, but not yet returned as updated."""
        self._checkOnDaddy()
        return list(self.jobs.keys())

    def getRunningBatchJobIDs(self):
        self._checkOnDaddy()
        now = time.time()
        return {jobID:now - info.time for jobID, info in list(self.runningJobs.items())}

    def shutdown(self):
        """
        Cleanly terminate and join daddy thread.
        """
        if self.daddyThread is not None:
            self.shuttingDown.set()
            self.daddyThread.join()
        BatchSystemSupport.workerCleanup(self.workerCleanupInfo)

    def getUpdatedBatchJob(self, maxWait):
        """Returns a tuple of a no-longer-running job, the return value of its process, and its runtime, or None."""
        self._checkOnDaddy()
        try:
            item = self.outputQueue.get(timeout=maxWait)
        except Empty:
            return
        else:
            self.jobs.pop(item.jobID)
            log.debug('Ran jobID: %s with exit value: %i', item.jobID, item.exitStatus)
            return item

    @classmethod
    def setOptions(cls, setOption):
        setOption('scale', default=1)


class Info(object):
    __doc__ = '\n    Record for a running job.\n\n    Stores the start time of the job, the Popen object representing its child\n    (or None), the tuple of (coreFractions, memory, disk) it is using (or\n    None), and whether the job is supposed to be being killed.\n    '

    def __init__(self, startTime, popen, resources, killIntended):
        self.time = startTime
        self.popen = popen
        self.resources = resources
        self.killIntended = killIntended


class ResourcePool(object):
    __doc__ = '\n    Represents an integral amount of a resource (such as memory bytes).\n\n    Amounts can be acquired immediately or with a timeout, and released.\n\n    Provides a context manager to do something with an amount of resource\n    acquired.\n    '

    def __init__(self, initial_value, resourceType, timeout=5):
        super(ResourcePool, self).__init__()
        self.condition = Condition()
        self.value = initial_value
        self.resourceType = resourceType
        self.timeout = timeout

    def acquireNow(self, amount):
        """
        Reserve the given amount of the given resource.

        Returns True if successful and False if this is not possible immediately.
        """
        with self.condition:
            if amount > self.value:
                return False
            else:
                self.value -= amount
                self._ResourcePool__validate()
                return True

    def acquire(self, amount):
        """
        Reserve the given amount of the given resource.

        Raises AcquisitionTimeoutException if this is not possible in under
        self.timeout time.
        """
        with self.condition:
            startTime = time.time()
            while amount > self.value:
                if time.time() - startTime >= self.timeout:
                    raise self.AcquisitionTimeoutException(resource=(self.resourceType), requested=amount,
                      available=(self.value))
                self.condition.wait(timeout=(self.timeout))

            self.value -= amount
            self._ResourcePool__validate()

    def release(self, amount):
        with self.condition:
            self.value += amount
            self._ResourcePool__validate()
            self.condition.notify_all()

    def __validate(self):
        assert 0 <= self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'ResourcePool(%i)' % self.value

    @contextmanager
    def acquisitionOf(self, amount):
        self.acquire(amount)
        try:
            yield
        finally:
            self.release(amount)

    class AcquisitionTimeoutException(Exception):
        __doc__ = 'To be raised when a resource request times out.'

        def __init__(self, resource, requested, available):
            """
            Creates an instance of this exception that indicates which resource is insufficient for
            current demands, as well as the amount requested and amount actually available.

            :param str resource: string representing the resource type

            :param int|float requested: the amount of the particular resource requested that resulted
                   in this exception

            :param int|float available: amount of the particular resource actually available
            """
            self.requested = requested
            self.available = available
            self.resource = resource