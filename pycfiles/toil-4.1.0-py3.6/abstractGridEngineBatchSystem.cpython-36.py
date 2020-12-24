# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/abstractGridEngineBatchSystem.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 16902 bytes
from __future__ import absolute_import
from builtins import str
from datetime import datetime
import logging, time
from threading import Thread, Lock
from abc import ABCMeta, abstractmethod
from six.moves.queue import Empty, Queue
from future.utils import with_metaclass
from toil.lib.misc import CalledProcessErrorStderr
from toil.lib.objects import abstractclassmethod
from toil.batchSystems.abstractBatchSystem import BatchSystemLocalSupport, UpdatedBatchJobInfo
logger = logging.getLogger(__name__)

class AbstractGridEngineBatchSystem(BatchSystemLocalSupport):
    __doc__ = '\n    A partial implementation of BatchSystemSupport for batch systems run on a\n    standard HPC cluster. By default worker cleanup and auto-deployment are not\n    implemented.\n    '

    class Worker(with_metaclass(ABCMeta, Thread)):

        def __init__(self, newJobsQueue, updatedJobsQueue, killQueue, killedJobsQueue, boss):
            """
            Abstract worker interface class. All instances are created with five
            initial arguments (below). Note the Queue instances passed are empty.

            :param newJobsQueue: a Queue of new (unsubmitted) jobs
            :param updatedJobsQueue: a Queue of jobs that have been updated
            :param killQueue: a Queue of active jobs that need to be killed
            :param killedJobsQueue: Queue of killed jobs for this worker
            :param boss: the AbstractGridEngineBatchSystem instance that
                         controls this AbstractGridEngineWorker

            """
            Thread.__init__(self)
            self.boss = boss
            self.boss.config.statePollingWait = self.boss.config.statePollingWait or self.boss.getWaitDuration()
            self.newJobsQueue = newJobsQueue
            self.updatedJobsQueue = updatedJobsQueue
            self.killQueue = killQueue
            self.killedJobsQueue = killedJobsQueue
            self.waitingJobs = list()
            self.runningJobs = set()
            self.runningJobsLock = Lock()
            self.batchJobIDs = dict()
            self._checkOnJobsCache = None
            self._checkOnJobsTimestamp = None

        def getBatchSystemID(self, jobID):
            """
            Get batch system-specific job ID

            Note: for the moment this is the only consistent way to cleanly get
            the batch system job ID

            :param: string jobID: toil job ID
            """
            if jobID not in self.batchJobIDs:
                raise RuntimeError('Unknown jobID, could not be converted')
            job, task = self.batchJobIDs[jobID]
            if task is None:
                return str(job)
            else:
                return str(job) + '.' + str(task)

        def forgetJob(self, jobID):
            """
            Remove jobID passed

            :param: string jobID: toil job ID
            """
            with self.runningJobsLock:
                self.runningJobs.remove(jobID)
            del self.batchJobIDs[jobID]

        def createJobs(self, newJob):
            """
            Create a new job with the Toil job ID.

            Implementation-specific; called by AbstractGridEngineWorker.run()

            :param string newJob: Toil job ID
            """
            activity = False
            if newJob is not None:
                self.waitingJobs.append(newJob)
            while len(self.waitingJobs) > 0 and len(self.runningJobs) < int(self.boss.config.maxLocalJobs):
                activity = True
                jobID, cpu, memory, command, jobName = self.waitingJobs.pop(0)
                subLine = self.prepareSubmission(cpu, memory, jobID, command, jobName)
                logger.debug('Running %r', subLine)
                batchJobID = self.boss.with_retries(self.submitJob, subLine)
                logger.debug('Submitted job %s', str(batchJobID))
                self.batchJobIDs[jobID] = (
                 batchJobID, None)
                with self.runningJobsLock:
                    self.runningJobs.add(jobID)

            return activity

        def killJobs(self):
            """
            Kill any running jobs within worker
            """
            killList = list()
            while True:
                try:
                    jobId = self.killQueue.get(block=False)
                except Empty:
                    break
                else:
                    killList.append(jobId)

            if not killList:
                return False
            else:
                for jobID in list(killList):
                    if jobID in self.runningJobs:
                        logger.debug('Killing job: %s', jobID)
                        self.killJob(jobID)
                    else:
                        if jobID in self.waitingJobs:
                            self.waitingJobs.remove(jobID)
                        self.killedJobsQueue.put(jobID)
                        killList.remove(jobID)

                while killList:
                    for jobID in list(killList):
                        batchJobID = self.getBatchSystemID(jobID)
                        if self.boss.with_retries(self.getJobExitCode, batchJobID) is not None:
                            logger.debug('Adding jobID %s to killedJobsQueue', jobID)
                            self.killedJobsQueue.put(jobID)
                            killList.remove(jobID)
                            self.forgetJob(jobID)

                    if len(killList) > 0:
                        logger.warning("Some jobs weren't killed, trying again in %is.", self.boss.sleepSeconds())

                return True

        def checkOnJobs(self):
            """Check and update status of all running jobs.

            Respects statePollingWait and will return cached results if not within
            time period to talk with the scheduler.
            """
            if self._checkOnJobsTimestamp:
                if (datetime.now() - self._checkOnJobsTimestamp).total_seconds() < self.boss.config.statePollingWait:
                    return self._checkOnJobsCache
            activity = False
            for jobID in list(self.runningJobs):
                batchJobID = self.getBatchSystemID(jobID)
                status = self.boss.with_retries(self.getJobExitCode, batchJobID)
                if status is not None:
                    activity = True
                    self.updatedJobsQueue.put(UpdatedBatchJobInfo(jobID=jobID, exitStatus=status, exitReason=None, wallTime=None))
                    self.forgetJob(jobID)

            self._checkOnJobsCache = activity
            self._checkOnJobsTimestamp = datetime.now()
            return activity

        def _runStep(self):
            """return True if more jobs, False is all done"""
            activity = False
            newJob = None
            activity = self.newJobsQueue.empty() or True
            newJob = self.newJobsQueue.get()
            if newJob is None:
                logger.debug('Received queue sentinel.')
                return False
            else:
                activity |= self.killJobs()
                activity |= self.createJobs(newJob)
                activity |= self.checkOnJobs()
                if not activity:
                    logger.debug('No activity, sleeping for %is', self.boss.sleepSeconds())
                return True

        def run(self):
            """
            Run any new jobs
            """
            try:
                while self._runStep():
                    pass

            except Exception as ex:
                logger.error('GridEngine like batch system failure', exc_info=ex)
                raise

        @abstractmethod
        def prepareSubmission(self, cpu, memory, jobID, command, jobName):
            """
            Preparation in putting together a command-line string
            for submitting to batch system (via submitJob().)

            :param: string cpu
            :param: string memory
            :param: string jobID  : Toil job ID
            :param: string subLine: the command line string to be called
            :param: string jobName: the name of the Toil job, to provide metadata to batch systems if desired

            :rtype: string
            """
            raise NotImplementedError()

        @abstractmethod
        def submitJob(self, subLine):
            """
            Wrapper routine for submitting the actual command-line call, then
            processing the output to get the batch system job ID

            :param: string subLine: the literal command line string to be called

            :rtype: string: batch system job ID, which will be stored internally
            """
            raise NotImplementedError()

        @abstractmethod
        def getRunningJobIDs(self):
            """
            Get a list of running job IDs. Implementation-specific; called by boss
            AbstractGridEngineBatchSystem implementation via
            AbstractGridEngineBatchSystem.getRunningBatchJobIDs()

            :rtype: list
            """
            raise NotImplementedError()

        @abstractmethod
        def killJob(self, jobID):
            """
            Kill specific job with the Toil job ID. Implementation-specific; called
            by AbstractGridEngineWorker.killJobs()

            :param string jobID: Toil job ID
            """
            raise NotImplementedError()

        @abstractmethod
        def getJobExitCode(self, batchJobID):
            """
            Returns job exit code. Implementation-specific; called by
            AbstractGridEngineWorker.checkOnJobs()

            :param string batchjobID: batch system job ID
            """
            raise NotImplementedError()

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(AbstractGridEngineBatchSystem, self).__init__(config, maxCores, maxMemory, maxDisk)
        self.config = config
        self.currentJobs = set()
        self.maxCPU, self.maxMEM = self.obtainSystemConstants()
        self.newJobsQueue = Queue()
        self.updatedJobsQueue = Queue()
        self.killQueue = Queue()
        self.killedJobsQueue = Queue()
        self.worker = self.Worker(self.newJobsQueue, self.updatedJobsQueue, self.killQueue, self.killedJobsQueue, self)
        self.worker.start()
        self._getRunningBatchJobIDsTimestamp = None
        self._getRunningBatchJobIDsCache = {}

    @classmethod
    def supportsWorkerCleanup(cls):
        return False

    @classmethod
    def supportsAutoDeployment(cls):
        return False

    def issueBatchJob(self, jobNode):
        localID = self.handleLocalJob(jobNode)
        if localID:
            return localID
        else:
            self.checkResourceRequest(jobNode.memory, jobNode.cores, jobNode.disk)
            jobID = self.getNextJobID()
            self.currentJobs.add(jobID)
            self.newJobsQueue.put((jobID, jobNode.cores, jobNode.memory, jobNode.command, jobNode.jobName))
            logger.debug('Issued the job command: %s with job id: %s and job name %s', jobNode.command, str(jobID), jobNode.jobName)
            return jobID

    def killBatchJobs(self, jobIDs):
        """
        Kills the given jobs, represented as Job ids, then checks they are dead by checking
        they are not in the list of issued jobs.
        """
        self.killLocalJobs(jobIDs)
        jobIDs = set(jobIDs)
        logger.debug('Jobs to be killed: %r', jobIDs)
        for jobID in jobIDs:
            self.killQueue.put(jobID)

        while jobIDs:
            killedJobId = self.killedJobsQueue.get()
            if killedJobId is None:
                break
            jobIDs.remove(killedJobId)
            if killedJobId in self.currentJobs:
                self.currentJobs.remove(killedJobId)
            if jobIDs:
                logger.debug('Some kills (%s) still pending, sleeping %is', len(jobIDs), self.sleepSeconds())

    def getIssuedBatchJobIDs(self):
        """
        Gets the list of issued jobs
        """
        return list(self.getIssuedLocalJobIDs()) + list(self.currentJobs)

    def getRunningBatchJobIDs(self):
        """
        Retrieve running job IDs from local and batch scheduler.

        Respects statePollingWait and will return cached results if not within
        time period to talk with the scheduler.
        """
        if self._getRunningBatchJobIDsTimestamp:
            if (datetime.now() - self._getRunningBatchJobIDsTimestamp).total_seconds() < self.config.statePollingWait:
                batchIds = self._getRunningBatchJobIDsCache
        else:
            batchIds = self.with_retries(self.worker.getRunningJobIDs)
            self._getRunningBatchJobIDsCache = batchIds
            self._getRunningBatchJobIDsTimestamp = datetime.now()
        batchIds.update(self.getRunningLocalJobIDs())
        return batchIds

    def getUpdatedBatchJob(self, maxWait):
        local_tuple = self.getUpdatedLocalJob(0)
        if local_tuple:
            return local_tuple
        try:
            item = self.updatedJobsQueue.get(timeout=maxWait)
        except Empty:
            return
        else:
            logger.debug('UpdatedJobsQueue Item: %s', item)
            self.currentJobs.remove(item.jobID)
            return item

    def shutdown(self):
        """
        Signals worker to shutdown (via sentinel) then cleanly joins the thread
        """
        self.shutdownLocal()
        newJobsQueue = self.newJobsQueue
        self.newJobsQueue = None
        newJobsQueue.put(None)
        self.worker.join()

    def setEnv(self, name, value=None):
        if value:
            if ',' in value:
                raise ValueError(type(self).__name__ + ' does not support commata in environment variable values')
        return super(AbstractGridEngineBatchSystem, self).setEnv(name, value)

    @classmethod
    def getWaitDuration(self):
        return 1

    def sleepSeconds(self, sleeptime=1):
        """ Helper function to drop on all state-querying functions to avoid over-querying.
        """
        time.sleep(sleeptime)
        return sleeptime

    @abstractclassmethod
    def obtainSystemConstants(cls):
        """
        Returns the max. memory and max. CPU for the system
        """
        raise NotImplementedError()

    def with_retries(self, operation, *args, **kwargs):
        """
        Call operation with args and kwargs. If one of the calls to an SGE
        command fails, sleep and try again for a set number of times.
        """
        maxTries = 3
        tries = 0
        while True:
            tries += 1
            try:
                return operation(*args, **kwargs)
            except CalledProcessErrorStderr as err:
                if tries < maxTries:
                    logger.error('Will retry errored operation %s, code %d: %s', operation.__name__, err.returncode, err.stderr)
                    time.sleep(self.config.statePollingWait)
                else:
                    logger.error('Failed operation %s, code %d: %s', operation.__name__, err.returncode, err.stderr)
                    raise err