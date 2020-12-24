# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/leader.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 59921 bytes
"""
The leader script (of the leader/worker pair) for running jobs.
"""
from __future__ import absolute_import
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from builtins import super
import logging, time, os, sys, glob
from toil.lib.humanize import bytes2human
from toil import resolveEntryPoint
try:
    from toil.cwl.cwltoil import CWL_INTERNAL_JOBS
except ImportError:
    CWL_INTERNAL_JOBS = ()

from toil.batchSystems.abstractBatchSystem import BatchJobExitReason
from toil.jobStores.abstractJobStore import NoSuchJobException
from toil.batchSystems import DeadlockException
from toil.lib.throttle import LocalThrottle
from toil.provisioners.clusterScaler import ScalerThread
from toil.serviceManager import ServiceManager
from toil.statsAndLogging import StatsAndLogging
from toil.job import JobNode, ServiceJobNode
from toil.toilState import ToilState
from toil.common import Toil, ToilMetrics
import enlighten
logger = logging.getLogger(__name__)

class FailedJobsException(Exception):

    def __init__(self, jobStoreLocator, failedJobs, jobStore):
        self.msg = "The job store '%s' contains %i failed jobs" % (jobStoreLocator, len(failedJobs))
        try:
            self.msg += ': %s' % ', '.join(str(failedJob) for failedJob in failedJobs)
            for jobNode in failedJobs:
                job = jobStore.load(jobNode.jobStoreID)
                if job.logJobStoreFileID:
                    with job.getLogFileHandle(jobStore) as (fH):
                        self.msg += '\n' + StatsAndLogging.formatLogStream(fH, jobNode)

        except:
            logger.exception('Exception when compiling information about failed jobs')

        self.msg = self.msg.rstrip('\n')
        super().__init__()
        self.jobStoreLocator = jobStoreLocator
        self.numberOfFailedJobs = len(failedJobs)

    def __str__(self):
        """
        Stringify the exception, including the message.
        """
        return self.msg


class Leader(object):
    __doc__ = ' Class that encapsulates the logic of the leader.\n    '

    def __init__(self, config, batchSystem, provisioner, jobStore, rootJob, jobCache=None):
        """
        :param toil.common.Config config:
        :param toil.batchSystems.abstractBatchSystem.AbstractBatchSystem batchSystem:
        :param toil.provisioners.abstractProvisioner.AbstractProvisioner provisioner
        :param toil.jobStores.abstractJobStore.AbstractJobStore jobStore:
        :param toil.jobGraph.JobGraph rootJob

        If jobCache is passed, it must be a dict from job ID to pre-existing
        JobGraph objects. Jobs will be loaded from the cache (which can be
        downloaded from the jobStore in a batch) during the construction of the ToilState object.
        """
        self.config = config
        self.jobStore = jobStore
        self.jobStoreLocator = config.jobStore
        self.toilState = ToilState(jobStore, rootJob, jobCache=jobCache)
        logger.debug('Found %s jobs to start and %i jobs with successors to run', len(self.toilState.updatedJobs), len(self.toilState.successorCounts))
        self.batchSystem = batchSystem
        assert len(self.batchSystem.getIssuedBatchJobIDs()) == 0
        logger.debug('Checked batch system has no running jobs and no updated jobs')
        self.jobBatchSystemIDToIssuedJob = {}
        self.preemptableJobsIssued = 0
        self.serviceJobsIssued = 0
        self.serviceJobsToBeIssued = []
        self.preemptableServiceJobsIssued = 0
        self.preemptableServiceJobsToBeIssued = []
        self.timeSinceJobsLastRescued = None
        self.reissueMissingJobs_missingHash = {}
        self.provisioner = provisioner
        self.clusterScaler = None
        if self.provisioner is not None:
            if len(self.provisioner.nodeTypes) > 0:
                self.clusterScaler = ScalerThread(self.provisioner, self, self.config)
        self.serviceManager = ServiceManager(jobStore, self.toilState)
        self.statsAndLogging = StatsAndLogging(self.jobStore, self.config)
        self.potentialDeadlockedJobs = set()
        self.potentialDeadlockTime = 0
        self.toilMetrics = None
        self.debugJobNames = ('CWLJob', 'CWLWorkflow', 'CWLScatter', 'CWLGather', 'ResolveIndirect')
        self.deadlockThrottler = LocalThrottle(self.config.deadlockCheckInterval)
        self.statusThrottler = LocalThrottle(self.config.statusWait)
        self.progress_overall = None
        self.progress_failed = None
        self.GOOD_COLOR = (0, 60, 108)
        self.BAD_COLOR = (253, 199, 0)
        self.PROGRESS_BAR_FORMAT = '{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:{len_total}d}/{total:d} ({count_1:d} failures) [{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]'

    def run(self):
        """
        This runs the leader process to issue and manage jobs.

        :raises: toil.leader.FailedJobsException if failed jobs remain after running.

        :return: The return value of the root job's run function.
        :rtype: Any
        """
        with enlighten.get_manager(stream=(sys.stderr), enabled=(not self.config.disableProgress)) as (manager):
            self.progress_overall = manager.counter(total=0, desc='Workflow Progress', unit='jobs', color=(self.GOOD_COLOR),
              bar_format=(self.PROGRESS_BAR_FORMAT))
            self.progress_failed = self.progress_overall.add_subcounter(self.BAD_COLOR)
            self.statsAndLogging.start()
            if self.config.metrics:
                self.toilMetrics = ToilMetrics(provisioner=(self.provisioner))
            try:
                self.serviceManager.start()
                try:
                    if self.clusterScaler is not None:
                        self.clusterScaler.start()
                    try:
                        self.innerLoop()
                    finally:
                        if self.clusterScaler is not None:
                            logger.debug('Waiting for workers to shutdown.')
                            startTime = time.time()
                            self.clusterScaler.shutdown()
                            logger.debug('Worker shutdown complete in %s seconds.', time.time() - startTime)

                finally:
                    self.serviceManager.shutdown()

            finally:
                self.statsAndLogging.shutdown()
                if self.toilMetrics:
                    self.toilMetrics.shutdown()

            self.toilState.totalFailedJobs = [j for j in self.toilState.totalFailedJobs if self.jobStore.exists(j.jobStoreID)]
            try:
                self.create_status_sentinel_file(self.toilState.totalFailedJobs)
            except IOError as e:
                logger.debug('Error from importFile with hardlink=True: {}'.format(e))

            logger.info('Finished toil run %s' % ('successfully.' if not self.toilState.totalFailedJobs else 'with %s failed jobs.' % len(self.toilState.totalFailedJobs)))
            if len(self.toilState.totalFailedJobs):
                logger.info('Failed jobs at end of the run: %s', ' '.join(str(job) for job in self.toilState.totalFailedJobs))
            if len(self.toilState.totalFailedJobs) > 0:
                raise FailedJobsException(self.config.jobStore, self.toilState.totalFailedJobs, self.jobStore)
            return self.jobStore.getRootJobReturnValue()

    def create_status_sentinel_file(self, fail):
        """Create a file in the jobstore indicating failure or success."""
        logName = 'failed.log' if fail else 'succeeded.log'
        localLog = os.path.join(os.getcwd(), logName)
        open(localLog, 'w').close()
        self.jobStore.importFile(('file://' + localLog), logName, hardlink=True)
        if os.path.exists(localLog):
            os.remove(localLog)

    def _handledFailedSuccessor(self, jobNode, jobGraph, successorJobStoreID):
        """Deal with the successor having failed. Return True if there are
        still active successors. Return False if all successors have failed
        and the job is queued to run to handle the failed successors."""
        logger.debug('Successor job: %s of job: %s has failed predecessors', jobNode, jobGraph)
        self.toilState.hasFailedSuccessors.add(jobGraph.jobStoreID)
        self.toilState.successorCounts[jobGraph.jobStoreID] -= 1
        assert self.toilState.successorCounts[jobGraph.jobStoreID] >= 0
        self.toilState.successorJobStoreIDToPredecessorJobs[successorJobStoreID].remove(jobGraph)
        if len(self.toilState.successorJobStoreIDToPredecessorJobs[successorJobStoreID]) == 0:
            self.toilState.successorJobStoreIDToPredecessorJobs.pop(successorJobStoreID)
        if self.toilState.successorCounts[jobGraph.jobStoreID] == 0:
            logger.debug('Job: %s has no successors to run and some are failed, adding to list of jobs with failed successors', jobGraph)
            self.toilState.successorCounts.pop(jobGraph.jobStoreID)
            self.toilState.updatedJobs.add((jobGraph, 0))
            return False

    def _checkSuccessorReadyToRunMultiplePredecessors(self, jobGraph, jobNode, successorJobStoreID):
        """Handle the special cases of checking if a successor job is
        ready to run when there are multiple predecessors"""
        logger.debug('Successor job: %s of job: %s has multiple predecessors', jobNode, jobGraph)
        if successorJobStoreID not in self.toilState.jobsToBeScheduledWithMultiplePredecessors:
            self.toilState.jobsToBeScheduledWithMultiplePredecessors[successorJobStoreID] = self.jobStore.load(successorJobStoreID)
        else:
            successorJobGraph = self.toilState.jobsToBeScheduledWithMultiplePredecessors[successorJobStoreID]
            successorJobGraph.predecessorsFinished.add(jobGraph.jobStoreID)
            if successorJobStoreID in self.toilState.failedSuccessors:
                if not self._handledFailedSuccessor(jobNode, jobGraph, successorJobStoreID):
                    return False
            assert len(successorJobGraph.predecessorsFinished) <= successorJobGraph.predecessorNumber
        if len(successorJobGraph.predecessorsFinished) < successorJobGraph.predecessorNumber:
            return False
        else:
            self.toilState.jobsToBeScheduledWithMultiplePredecessors.pop(successorJobStoreID)
            return True

    def _makeJobSuccessorReadyToRun(self, jobGraph, jobNode):
        """make a successor job ready to run, returning False if they should
        not yet be run"""
        successorJobStoreID = jobNode.jobStoreID
        if successorJobStoreID not in self.toilState.successorJobStoreIDToPredecessorJobs:
            self.toilState.successorJobStoreIDToPredecessorJobs[successorJobStoreID] = []
        self.toilState.successorJobStoreIDToPredecessorJobs[successorJobStoreID].append(jobGraph)
        if jobNode.predecessorNumber > 1:
            return self._checkSuccessorReadyToRunMultiplePredecessors(jobGraph, jobNode, successorJobStoreID)
        else:
            return True

    def _runJobSuccessors(self, jobGraph):
        if not len(jobGraph.stack[(-1)]) > 0:
            raise AssertionError
        else:
            logger.debug('Job: %s has %i successors to schedule', jobGraph.jobStoreID, len(jobGraph.stack[(-1)]))
            assert jobGraph.jobStoreID not in self.toilState.successorCounts
        self.toilState.successorCounts[jobGraph.jobStoreID] = len(jobGraph.stack[(-1)])
        successors = []
        for jobNode in jobGraph.stack[(-1)]:
            if self._makeJobSuccessorReadyToRun(jobGraph, jobNode):
                successors.append(jobNode)

        self.issueJobs(successors)

    def _processFailedSuccessors(self, jobGraph):
        """Some of the jobs successors failed then either fail the job
        or restart it if it has retries left and is a checkpoint job"""
        if jobGraph.jobStoreID in self.toilState.servicesIssued:
            logger.debug('Telling job: %s to terminate its services due to successor failure', jobGraph.jobStoreID)
            self.serviceManager.killServices((self.toilState.servicesIssued[jobGraph.jobStoreID]), error=True)
        else:
            if jobGraph.jobStoreID in self.toilState.successorCounts:
                logger.debug('Job %s with ID: %s with failed successors still has successor jobs running', jobGraph, jobGraph.jobStoreID)
            elif jobGraph.checkpoint is not None:
                if jobGraph.remainingRetryCount > 1:
                    logger.warning('Job: %s is being restarted as a checkpoint after the total failure of jobs in its subtree.', jobGraph.jobStoreID)
                    self.issueJob(JobNode.fromJobGraph(jobGraph))
            else:
                logger.debug('Job %s is being processed as completely failed', jobGraph.jobStoreID)
                self.processTotallyFailedJob(jobGraph)

    def _processReadyJob(self, jobGraph, resultStatus):
        logger.debug('Updating status of job %s with ID %s: with result status: %s', jobGraph, jobGraph.jobStoreID, resultStatus)
        if jobGraph in self.serviceManager.jobGraphsWithServicesBeingStarted:
            logger.debug('Got a job to update which is still owned by the service manager: %s', jobGraph.jobStoreID)
        else:
            if jobGraph.jobStoreID in self.toilState.hasFailedSuccessors:
                self._processFailedSuccessors(jobGraph)
            else:
                if jobGraph.command is not None or resultStatus != 0:
                    isServiceJob = jobGraph.jobStoreID in self.toilState.serviceJobStoreIDToPredecessorJob
                    if jobGraph.remainingRetryCount == 0 or isServiceJob and not self.jobStore.fileExists(jobGraph.errorJobStoreID):
                        self.processTotallyFailedJob(jobGraph)
                        logger.warning('Job %s with ID %s is completely failed', jobGraph, jobGraph.jobStoreID)
                    else:
                        self.issueJob(JobNode.fromJobGraph(jobGraph))
                else:
                    if len(jobGraph.services) > 0:
                        assert jobGraph.jobStoreID not in self.toilState.servicesIssued
                        self.toilState.servicesIssued[jobGraph.jobStoreID] = {}
                        for serviceJobList in jobGraph.services:
                            for serviceTuple in serviceJobList:
                                serviceID = serviceTuple.jobStoreID
                                assert serviceID not in self.toilState.serviceJobStoreIDToPredecessorJob
                                self.toilState.serviceJobStoreIDToPredecessorJob[serviceID] = jobGraph
                                self.toilState.servicesIssued[jobGraph.jobStoreID][serviceID] = serviceTuple

                        self.serviceManager.scheduleServices(jobGraph)
                        logger.debug('Giving job: %s to service manager to schedule its jobs', jobGraph.jobStoreID)
                    else:
                        if len(jobGraph.stack) > 0:
                            self._runJobSuccessors(jobGraph)
                        else:
                            if jobGraph.jobStoreID in self.toilState.servicesIssued:
                                logger.debug('Telling job: %s to terminate its services due to the successful completion of its successor jobs', jobGraph)
                                self.serviceManager.killServices((self.toilState.servicesIssued[jobGraph.jobStoreID]), error=False)
                            else:
                                if jobGraph.remainingRetryCount > 0:
                                    self.issueJob(JobNode.fromJobGraph(jobGraph))
                                    logger.debug('Job: %s is empty, we are scheduling to clean it up', jobGraph.jobStoreID)
                                else:
                                    self.processTotallyFailedJob(jobGraph)
                                    logger.warning('Job: %s is empty but completely failed - something is very wrong', jobGraph.jobStoreID)

    def _processReadyJobs(self):
        """Process jobs that are ready to be scheduled/have successors to schedule"""
        logger.debug('Built the jobs list, currently have %i jobs to update and %i jobs issued', len(self.toilState.updatedJobs), self.getNumberOfJobsIssued())
        updatedJobs = self.toilState.updatedJobs
        self.toilState.updatedJobs = set()
        for jobGraph, resultStatus in updatedJobs:
            self._processReadyJob(jobGraph, resultStatus)

    def _startServiceJobs(self):
        """Start any service jobs available from the service manager"""
        self.issueQueingServiceJobs()
        while True:
            serviceJob = self.serviceManager.getServiceJobsToStart(0)
            if serviceJob is None:
                break
            logger.debug('Launching service job: %s', serviceJob)
            self.issueServiceJob(serviceJob)

    def _processJobsWithRunningServices(self):
        """Get jobs whose services have started"""
        while True:
            jobGraph = self.serviceManager.getJobGraphWhoseServicesAreRunning(0)
            if jobGraph is None:
                break
            logger.debug('Job: %s has established its services.', jobGraph.jobStoreID)
            jobGraph.services = []
            self.toilState.updatedJobs.add((jobGraph, 0))

    def _gatherUpdatedJobs(self, updatedJobTuple):
        """Gather any new, updated jobGraph from the batch system"""
        jobID, exitStatus, exitReason, wallTime = (
         updatedJobTuple.jobID, updatedJobTuple.exitStatus, updatedJobTuple.exitReason,
         updatedJobTuple.wallTime)
        try:
            updatedJob = self.jobBatchSystemIDToIssuedJob[jobID]
        except KeyError:
            logger.warning('A result seems to already have been processed for job %s', jobID)
        else:
            if exitStatus == 0:
                cur_logger = logger.debug if str(updatedJob.jobName).startswith(CWL_INTERNAL_JOBS) else logger.info
                cur_logger('Job ended: %s', updatedJob)
                if self.toilMetrics:
                    self.toilMetrics.logCompletedJob(updatedJob)
            else:
                logger.warning('Job failed with exit value %i: %s', exitStatus, updatedJob)
            self.processFinishedJob(jobID, exitStatus, wallTime=wallTime, exitReason=exitReason)

    def _processLostJobs(self):
        """Process jobs that have gone awry"""
        if time.time() - self.timeSinceJobsLastRescued >= self.config.rescueJobsFrequency:
            self.reissueOverLongJobs()
            hasNoMissingJobs = self.reissueMissingJobs()
            if hasNoMissingJobs:
                self.timeSinceJobsLastRescued = time.time()
            else:
                self.timeSinceJobsLastRescued += 60

    def innerLoop(self):
        """
        The main loop for processing jobs by the leader.
        """
        self.timeSinceJobsLastRescued = time.time()
        while self.toilState.updatedJobs or self.getNumberOfJobsIssued() or self.serviceManager.jobsIssuedToServiceManager:
            if self.toilState.updatedJobs:
                self._processReadyJobs()
            else:
                self._startServiceJobs()
                self._processJobsWithRunningServices()
                updatedJobTuple = self.batchSystem.getUpdatedBatchJob(maxWait=2)
                if updatedJobTuple is not None:
                    self._gatherUpdatedJobs(updatedJobTuple)
                else:
                    self._processLostJobs()
                self.statsAndLogging.check()
                self.serviceManager.check()
                if self.clusterScaler is not None:
                    self.clusterScaler.check()
                if len(self.toilState.updatedJobs) == 0:
                    if self.deadlockThrottler.throttle(wait=False):
                        self.checkForDeadlocks()
                if self.statusThrottler.throttle(wait=False):
                    self._reportWorkflowStatus()
            self.progress_overall.update(incr=0)

        logger.debug('Finished the main loop: no jobs left to run.')
        if not self.toilState.updatedJobs == set():
            raise AssertionError
        else:
            if not self.toilState.successorCounts == {}:
                raise AssertionError
            else:
                assert self.toilState.successorJobStoreIDToPredecessorJobs == {}
                assert self.toilState.serviceJobStoreIDToPredecessorJob == {}
            assert self.toilState.servicesIssued == {}

    def checkForDeadlocks(self):
        """
        Checks if the system is deadlocked running service jobs.
        """
        totalRunningJobs = len(self.batchSystem.getRunningBatchJobIDs())
        totalServicesIssued = self.serviceJobsIssued + self.preemptableServiceJobsIssued
        if totalServicesIssued >= totalRunningJobs and totalRunningJobs > 0:
            serviceJobs = [x for x in list(self.jobBatchSystemIDToIssuedJob.keys()) if isinstance(self.jobBatchSystemIDToIssuedJob[x], ServiceJobNode)]
            runningServiceJobs = set([x for x in serviceJobs if self.serviceManager.isRunning(self.jobBatchSystemIDToIssuedJob[x])])
            assert len(runningServiceJobs) <= totalRunningJobs
            if len(runningServiceJobs) == totalRunningJobs:
                message = self.batchSystem.getSchedulingStatusMessage()
                if message is not None:
                    message = 'The batch system reports: {}'.format(message)
                else:
                    message = 'Cluster may be too small.'
                if self.potentialDeadlockedJobs != runningServiceJobs:
                    logger.warning('Potential deadlock detected! All %s running jobs are service jobs, with no normal jobs to use them! %s', totalRunningJobs, message)
                    self.potentialDeadlockedJobs = runningServiceJobs
                    self.potentialDeadlockTime = time.time()
                else:
                    stuckFor = time.time() - self.potentialDeadlockTime
                    if stuckFor >= self.config.deadlockWait:
                        logger.error('We have been deadlocked since %s on these service jobs: %s', self.potentialDeadlockTime, self.potentialDeadlockedJobs)
                        raise DeadlockException('The workflow is service deadlocked - all %d running jobs have been the same active services for at least %s seconds' % (
                         totalRunningJobs, self.config.deadlockWait))
                    else:
                        waitingNormalJobs = self.getNumberOfJobsIssued() - totalServicesIssued
                        logger.warning('Potentially deadlocked for %.0f seconds. Waiting at most %.0f more seconds for any of %d issued non-service jobs to schedule and start. %s', stuckFor, self.config.deadlockWait - stuckFor, waitingNormalJobs, message)
            else:
                if len(self.potentialDeadlockedJobs) > 0:
                    logger.warning('Potential deadlock has been resolved; non-service jobs are now running.')
                self.potentialDeadlockedJobs = set()
                self.potentialDeadlockTime = 0
        else:
            if len(self.potentialDeadlockedJobs) > 0:
                logger.warning('Potential deadlock has been resolved; non-service jobs are now running.')
            self.potentialDeadlockedJobs = set()
            self.potentialDeadlockTime = 0

    def issueJob(self, jobNode):
        """Add a job to the queue of jobs."""
        jobNode.command = ' '.join((resolveEntryPoint('_toil_worker'),
         jobNode.jobName,
         self.jobStoreLocator,
         jobNode.jobStoreID))
        jobBatchSystemID = self.batchSystem.issueBatchJob(jobNode)
        self.jobBatchSystemIDToIssuedJob[jobBatchSystemID] = jobNode
        if jobNode.preemptable:
            self.preemptableJobsIssued += 1
        cur_logger = logger.debug if jobNode.jobName.startswith(CWL_INTERNAL_JOBS) else logger.info
        cur_logger('Issued job %s with job batch system ID: %s and cores: %s, disk: %s, and memory: %s', jobNode, str(jobBatchSystemID), int(jobNode.cores), bytes2human(jobNode.disk), bytes2human(jobNode.memory))
        if self.toilMetrics:
            self.toilMetrics.logIssuedJob(jobNode)
            self.toilMetrics.logQueueSize(self.getNumberOfJobsIssued())
        self.progress_overall.total += 1
        self.progress_overall.update(incr=0)

    def issueJobs(self, jobs):
        """Add a list of jobs, each represented as a jobNode object."""
        for job in jobs:
            self.issueJob(job)

    def issueServiceJob(self, jobNode):
        """
        Issue a service job, putting it on a queue if the maximum number of service
        jobs to be scheduled has been reached.
        """
        if jobNode.preemptable:
            self.preemptableServiceJobsToBeIssued.append(jobNode)
        else:
            self.serviceJobsToBeIssued.append(jobNode)
        self.issueQueingServiceJobs()

    def issueQueingServiceJobs(self):
        """Issues any queuing service jobs up to the limit of the maximum allowed."""
        while len(self.serviceJobsToBeIssued) > 0 and self.serviceJobsIssued < self.config.maxServiceJobs:
            self.issueJob(self.serviceJobsToBeIssued.pop())
            self.serviceJobsIssued += 1

        while len(self.preemptableServiceJobsToBeIssued) > 0 and self.preemptableServiceJobsIssued < self.config.maxPreemptableServiceJobs:
            self.issueJob(self.preemptableServiceJobsToBeIssued.pop())
            self.preemptableServiceJobsIssued += 1

    def getNumberOfJobsIssued(self, preemptable=None):
        """
        Gets number of jobs that have been added by issueJob(s) and not
        removed by removeJob

        :param None or boolean preemptable: If none, return all types of jobs.
          If true, return just the number of preemptable jobs. If false, return
          just the number of non-preemptable jobs.
        """
        if preemptable is None:
            return len(self.jobBatchSystemIDToIssuedJob)
        else:
            if preemptable:
                return self.preemptableJobsIssued
            elif not len(self.jobBatchSystemIDToIssuedJob) >= self.preemptableJobsIssued:
                raise AssertionError
            return len(self.jobBatchSystemIDToIssuedJob) - self.preemptableJobsIssued

    def _getStatusHint(self):
        """
        Get a short string describing the current state of the workflow for a human.
        
        Should include number of currently running jobs, number of issued jobs, etc.
        
        Don't call this too often; it will talk to the batch system, which may
        make queries of the backing scheduler.
        
        :return: A one-line description of the current status of the workflow.
        :rtype: str
        """
        issuedJobCount = self.getNumberOfJobsIssued()
        runningJobCount = len(self.batchSystem.getRunningBatchJobIDs())
        return '%d jobs are running, %d jobs are issued and waiting to run' % (runningJobCount, issuedJobCount - runningJobCount)

    def _reportWorkflowStatus(self):
        """
        Report the current status of the workflow to the user.
        """
        logger.info(self._getStatusHint())

    def removeJob(self, jobBatchSystemID):
        """Removes a job from the system."""
        if not jobBatchSystemID in self.jobBatchSystemIDToIssuedJob:
            raise AssertionError
        else:
            jobNode = self.jobBatchSystemIDToIssuedJob[jobBatchSystemID]
            if jobNode.preemptable:
                assert self.preemptableJobsIssued > 0
                self.preemptableJobsIssued -= 1
            del self.jobBatchSystemIDToIssuedJob[jobBatchSystemID]
            if jobNode.jobStoreID in self.toilState.serviceJobStoreIDToPredecessorJob:
                if jobNode.preemptable:
                    self.preemptableServiceJobsIssued -= 1
                else:
                    self.serviceJobsIssued -= 1
        self.progress_overall.update(incr=1)
        return jobNode

    def getJobs(self, preemptable=None):
        jobs = self.jobBatchSystemIDToIssuedJob.values()
        if preemptable is not None:
            jobs = [job for job in jobs if job.preemptable == preemptable]
        return jobs

    def killJobs(self, jobsToKill):
        """
        Kills the given set of jobs and then sends them for processing.
        
        Returns the jobs that, upon processing, were reissued.
        """
        jobsRerunning = []
        if len(jobsToKill) > 0:
            self.batchSystem.killBatchJobs(jobsToKill)
            for jobBatchSystemID in jobsToKill:
                willRerun = self.processFinishedJob(jobBatchSystemID, 1, exitReason=(BatchJobExitReason.KILLED))
                if willRerun:
                    jobsRerunning.append(jobBatchSystemID)

        return jobsRerunning

    def reissueOverLongJobs(self):
        """
        Check each issued job - if it is running for longer than desirable
        issue a kill instruction.
        Wait for the job to die then we pass the job to processFinishedJob.
        """
        maxJobDuration = self.config.maxJobDuration
        jobsToKill = []
        if maxJobDuration < 10000000:
            runningJobs = self.batchSystem.getRunningBatchJobIDs()
            for jobBatchSystemID in list(runningJobs.keys()):
                if runningJobs[jobBatchSystemID] > maxJobDuration:
                    logger.warning("The job: %s has been running for: %s seconds, more than the max job duration: %s, we'll kill it", str(self.jobBatchSystemIDToIssuedJob[jobBatchSystemID].jobStoreID), str(runningJobs[jobBatchSystemID]), str(maxJobDuration))
                    jobsToKill.append(jobBatchSystemID)

            reissued = self.killJobs(jobsToKill)
            if len(jobsToKill) > 0:
                logger.info('Killed %d over long jobs and reissued %d of them', len(jobsToKill), len(reissued))

    def reissueMissingJobs(self, killAfterNTimesMissing=3):
        """
        Check all the current job ids are in the list of currently issued batch system jobs.
        If a job is missing, we mark it as so, if it is missing for a number of runs of
        this function (say 10).. then we try deleting the job (though its probably lost), we wait
        then we pass the job to processFinishedJob.
        """
        issuedJobs = set(self.batchSystem.getIssuedBatchJobIDs())
        jobBatchSystemIDsSet = set(list(self.jobBatchSystemIDToIssuedJob.keys()))
        missingJobIDsSet = set(list(self.reissueMissingJobs_missingHash.keys()))
        for jobBatchSystemID in missingJobIDsSet.difference(jobBatchSystemIDsSet):
            self.reissueMissingJobs_missingHash.pop(jobBatchSystemID)
            logger.warning('Batch system id: %s is no longer missing', str(jobBatchSystemID))

        assert issuedJobs.issubset(jobBatchSystemIDsSet)
        jobsToKill = []
        for jobBatchSystemID in set(jobBatchSystemIDsSet.difference(issuedJobs)):
            jobStoreID = self.jobBatchSystemIDToIssuedJob[jobBatchSystemID].jobStoreID
            if jobBatchSystemID in self.reissueMissingJobs_missingHash:
                self.reissueMissingJobs_missingHash[jobBatchSystemID] += 1
            else:
                self.reissueMissingJobs_missingHash[jobBatchSystemID] = 1
            timesMissing = self.reissueMissingJobs_missingHash[jobBatchSystemID]
            logger.warning('Job store ID %s with batch system id %s is missing for the %i time', jobStoreID, str(jobBatchSystemID), timesMissing)
            if self.toilMetrics:
                self.toilMetrics.logMissingJob()
            if timesMissing == killAfterNTimesMissing:
                self.reissueMissingJobs_missingHash.pop(jobBatchSystemID)
                jobsToKill.append(jobBatchSystemID)

        self.killJobs(jobsToKill)
        return len(self.reissueMissingJobs_missingHash) == 0

    def processRemovedJob(self, issuedJob, resultStatus):
        if resultStatus != 0:
            logger.warning('Despite the batch system claiming failure the job %s seems to have finished and been removed', issuedJob)
        self._updatePredecessorStatus(issuedJob.jobStoreID)

    def processFinishedJob(self, batchSystemID, resultStatus, wallTime=None, exitReason=None):
        """
        Function reads a processed jobGraph file and updates its state.
        
        Return True if the job is going to run again, and False if the job is
        fully done or completely failed.
        """
        jobNode = self.removeJob(batchSystemID)
        jobStoreID = jobNode.jobStoreID
        if wallTime is not None:
            if self.clusterScaler is not None:
                self.clusterScaler.addCompletedJob(jobNode, wallTime)
        if self.jobStore.exists(jobStoreID):
            logger.debug('Job %s continues to exist (i.e. has more to do)', jobNode)
            try:
                jobGraph = self.jobStore.load(jobStoreID)
            except NoSuchJobException:
                if self.jobStore.__class__.__name__ == 'AWSJobStore':
                    logger.warning('Got a stale read from SDB for job %s', jobNode)
                    self.processRemovedJob(jobNode, resultStatus)
                    return
                raise

            if jobGraph.logJobStoreFileID is not None:
                with jobGraph.getLogFileHandle(self.jobStore) as (logFileStream):
                    StatsAndLogging.logWithFormatting(jobStoreID, logFileStream, method=(logger.warning), message=('The job seems to have left a log file, indicating failure: %s' % jobGraph))
                if self.config.writeLogs or self.config.writeLogsGzip:
                    with jobGraph.getLogFileHandle(self.jobStore) as (logFileStream):
                        StatsAndLogging.writeLogFiles((jobGraph.chainedJobs), logFileStream, (self.config), failed=True)
            if resultStatus != 0:
                if jobGraph.logJobStoreFileID is None:
                    logger.warning('No log file is present, despite job failing: %s', jobNode)
                workDir = Toil.getToilWorkDir(self.config.workDir)
                batchSystemFilePrefix = 'toil_workflow_{}_job_{}_batch_'.format(self.config.workflowID, batchSystemID)
                batchSystemFileGlob = os.path.join(workDir, batchSystemFilePrefix + '*.log')
                batchSystemFiles = glob.glob(batchSystemFileGlob)
                for batchSystemFile in batchSystemFiles:
                    try:
                        batchSystemFileStream = open(batchSystemFile, 'rb')
                    except:
                        logger.warning('The batch system left a file %s, but it could not be opened' % batchSystemFile)
                    else:
                        with batchSystemFileStream:
                            if os.path.getsize(batchSystemFile) > 0:
                                StatsAndLogging.logWithFormatting(jobStoreID, batchSystemFileStream, method=(logger.warning), message=('The batch system left a non-empty file %s:' % batchSystemFile))
                                if self.config.writeLogs or self.config.writeLogsGzip:
                                    batchSystemFileRoot, _ = os.path.splitext(os.path.basename(batchSystemFile))
                                    jobNames = jobGraph.chainedJobs
                                    if jobNames is None:
                                        jobNames = [
                                         str(jobGraph)]
                                    jobNames = [jobName + '_' + batchSystemFileRoot for jobName in jobNames]
                                    batchSystemFileStream.seek(0)
                                    StatsAndLogging.writeLogFiles(jobNames, batchSystemFileStream, (self.config), failed=True)
                            else:
                                logger.warning('The batch system left an empty file %s' % batchSystemFile)

                jobGraph.setupJobAfterFailure((self.config), exitReason=exitReason)
                self.jobStore.update(jobGraph)
                self.progress_overall.update(incr=(-1))
                self.progress_failed.update(incr=1)
            else:
                if jobStoreID in self.toilState.hasFailedSuccessors:
                    self.toilState.hasFailedSuccessors.remove(jobStoreID)
            self.toilState.updatedJobs.add((jobGraph, resultStatus))
            logger.debug('Added job: %s to active jobs', jobGraph)
            return jobGraph.remainingRetryCount > 0
        else:
            self.processRemovedJob(jobNode, resultStatus)
            return False

    @staticmethod
    def getSuccessors(jobGraph, alreadySeenSuccessors, jobStore):
        """
        Gets successors of the given job by walking the job graph recursively.
        Any successor in alreadySeenSuccessors is ignored and not traversed.
        Returns the set of found successors. This set is added to alreadySeenSuccessors.
        """
        successors = set()

        def successorRecursion(jobGraph):
            for successorList in jobGraph.stack:
                for successorJobNode in successorList:
                    if successorJobNode.jobStoreID not in alreadySeenSuccessors:
                        successors.add(successorJobNode.jobStoreID)
                        alreadySeenSuccessors.add(successorJobNode.jobStoreID)
                        if jobStore.exists(successorJobNode.jobStoreID):
                            successorRecursion(jobStore.load(successorJobNode.jobStoreID))

        successorRecursion(jobGraph)
        return successors

    def processTotallyFailedJob(self, jobGraph):
        """
        Processes a totally failed job.
        """
        self.toilState.totalFailedJobs.add(JobNode.fromJobGraph(jobGraph))
        if self.toilMetrics:
            self.toilMetrics.logFailedJob(jobGraph)
        if jobGraph.jobStoreID in self.toilState.serviceJobStoreIDToPredecessorJob:
            logger.debug('Service job is being processed as a totally failed job: %s', jobGraph)
            predecesssorJobGraph = self.toilState.serviceJobStoreIDToPredecessorJob[jobGraph.jobStoreID]
            self._updatePredecessorStatus(jobGraph.jobStoreID)
            self.jobStore.deleteFile(jobGraph.startJobStoreID)
            if predecesssorJobGraph.jobStoreID in self.toilState.servicesIssued:
                self.serviceManager.killServices((self.toilState.servicesIssued[predecesssorJobGraph.jobStoreID]), error=True)
                logger.debug('Job: %s is instructing all the services of its parent job to quit', jobGraph)
            self.toilState.hasFailedSuccessors.add(predecesssorJobGraph.jobStoreID)
        else:
            assert jobGraph.jobStoreID not in self.toilState.servicesIssued
            unseenSuccessors = self.getSuccessors(jobGraph, self.toilState.failedSuccessors, self.jobStore)
            logger.debug('Found new failed successors: %s of job: %s', ' '.join(unseenSuccessors), jobGraph)
            for successorJobStoreID in unseenSuccessors:
                if successorJobStoreID in self.toilState.successorJobStoreIDToPredecessorJobs:
                    for predecessorJob in self.toilState.successorJobStoreIDToPredecessorJobs.pop(successorJobStoreID):
                        self.toilState.successorCounts[predecessorJob.jobStoreID] -= 1
                        self.toilState.hasFailedSuccessors.add(predecessorJob.jobStoreID)
                        logger.debug('Marking job: %s as having failed successors (found by reading successors failed job)', predecessorJob)
                        assert self.toilState.successorCounts[predecessorJob.jobStoreID] >= 0
                        if self.toilState.successorCounts[predecessorJob.jobStoreID] == 0:
                            self.toilState.updatedJobs.add((predecessorJob, 0))
                            self.toilState.successorCounts.pop(predecessorJob.jobStoreID)

        if jobGraph.jobStoreID in self.toilState.successorJobStoreIDToPredecessorJobs:
            for predecessorJobGraph in self.toilState.successorJobStoreIDToPredecessorJobs[jobGraph.jobStoreID]:
                self.toilState.hasFailedSuccessors.add(predecessorJobGraph.jobStoreID)
                logger.debug('Totally failed job: %s is marking direct predecessor: %s as having failed jobs', jobGraph, predecessorJobGraph)

            self._updatePredecessorStatus(jobGraph.jobStoreID)

    def _updatePredecessorStatus(self, jobStoreID):
        """
        Update status of predecessors for finished successor job.
        """
        if jobStoreID in self.toilState.serviceJobStoreIDToPredecessorJob:
            predecessorJob = self.toilState.serviceJobStoreIDToPredecessorJob.pop(jobStoreID)
            self.toilState.servicesIssued[predecessorJob.jobStoreID].pop(jobStoreID)
            if len(self.toilState.servicesIssued[predecessorJob.jobStoreID]) == 0:
                self.toilState.servicesIssued.pop(predecessorJob.jobStoreID)
                self.toilState.updatedJobs.add((predecessorJob, 0))
        else:
            if jobStoreID not in self.toilState.successorJobStoreIDToPredecessorJobs:
                if not len(self.toilState.updatedJobs) == 0:
                    raise AssertionError
                else:
                    assert len(self.toilState.successorJobStoreIDToPredecessorJobs) == 0
                    assert len(self.toilState.successorCounts) == 0
                logger.debug('Reached root job %s so no predecessors to clean up' % jobStoreID)
            else:
                logger.debug('Cleaning the predecessors of %s' % jobStoreID)
                for predecessorJob in self.toilState.successorJobStoreIDToPredecessorJobs.pop(jobStoreID):
                    self.toilState.successorCounts[predecessorJob.jobStoreID] -= 1
                    if self.toilState.successorCounts[predecessorJob.jobStoreID] == 0:
                        self.toilState.successorCounts.pop(predecessorJob.jobStoreID)
                        if predecessorJob.jobStoreID not in self.toilState.hasFailedSuccessors:
                            predecessorJob.stack.pop()
                        assert predecessorJob not in self.toilState.updatedJobs
                        self.toilState.updatedJobs.add((predecessorJob, 0))