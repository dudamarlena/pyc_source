# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/jobGraph.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 10579 bytes
from __future__ import absolute_import
import logging
from toil.batchSystems.abstractBatchSystem import BatchJobExitReason
from toil.job import JobNode
logger = logging.getLogger(__name__)

class JobGraph(JobNode):
    __doc__ = '\n    A class encapsulating the minimal state of a Toil job. Instances of this class are persisted\n    in the job store and held in memory by the master. The actual state of job objects in user\n    scripts is persisted separately since it may be much bigger than the state managed by this\n    class and should therefore only be held in memory for brief periods of time.\n    '

    def __init__(self, command, memory, cores, disk, unitName, jobName, preemptable, jobStoreID, remainingRetryCount, predecessorNumber, filesToDelete=None, predecessorsFinished=None, stack=None, services=None, startJobStoreID=None, terminateJobStoreID=None, errorJobStoreID=None, logJobStoreFileID=None, checkpoint=None, checkpointFilesToDelete=None, chainedJobs=None):
        requirements = {'memory':memory, 
         'cores':cores,  'disk':disk,  'preemptable':preemptable}
        super(JobGraph, self).__init__(command=command, requirements=requirements,
          unitName=unitName,
          jobName=jobName,
          jobStoreID=jobStoreID,
          predecessorNumber=predecessorNumber)
        self.remainingRetryCount = remainingRetryCount
        self.filesToDelete = filesToDelete or []
        self.predecessorNumber = predecessorNumber
        self.predecessorsFinished = predecessorsFinished or set()
        self.stack = stack or []
        self.logJobStoreFileID = logJobStoreFileID
        self.services = services or []
        self.terminateJobStoreID = terminateJobStoreID
        self.startJobStoreID = startJobStoreID
        self.errorJobStoreID = errorJobStoreID
        self.checkpoint = checkpoint
        self.checkpointFilesToDelete = checkpointFilesToDelete
        self.chainedJobs = chainedJobs

    def __hash__(self):
        return hash(self.jobStoreID)

    def setupJobAfterFailure(self, config, exitReason=None):
        """
        Reduce the remainingRetryCount if greater than zero and set the memory
        to be at least as big as the default memory (in case of exhaustion of memory,
        which is common).
        """
        if config.enableUnlimitedPreemptableRetries:
            if exitReason == BatchJobExitReason.LOST:
                logger.info('*Not* reducing retry count (%s) of job %s with ID %s', self.remainingRetryCount, self, self.jobStoreID)
            else:
                self.remainingRetryCount = max(0, self.remainingRetryCount - 1)
                logger.warning('Due to failure we are reducing the remaining retry count of job %s with ID %s to %s', self, self.jobStoreID, self.remainingRetryCount)
        else:
            if self.memory < config.defaultMemory:
                self._memory = config.defaultMemory
                logger.warning('We have increased the default memory of the failed job %s to %s bytes', self, self.memory)
            if self.disk < config.defaultDisk:
                self._disk = config.defaultDisk
                logger.warning('We have increased the disk of the failed job %s to the default of %s bytes', self, self.disk)

    def restartCheckpoint(self, jobStore):
        """Restart a checkpoint after the total failure of jobs in its subtree.

        Writes the changes to the jobStore immediately. All the
        checkpoint's successors will be deleted, but its retry count
        will *not* be decreased.

        Returns a list with the IDs of any successors deleted.
        """
        assert self.checkpoint is not None
        successorsDeleted = []
        if self.stack or self.services or self.command != None:
            if self.command != None:
                assert self.command == self.checkpoint
                logger.debug('Checkpoint job already has command set to run')
            else:
                self.command = self.checkpoint
            jobStore.update(self)
            if self.stack or self.services:
                logger.debug('Checkpoint job has unfinished successor jobs, deleting the jobs on the stack: %s, services: %s ' % (
                 self.stack, self.services))

                def recursiveDelete(jobGraph2):
                    for jobs in jobGraph2.stack + jobGraph2.services:
                        for jobNode in jobs:
                            if jobStore.exists(jobNode.jobStoreID):
                                recursiveDelete(jobStore.load(jobNode.jobStoreID))
                            else:
                                logger.debug('Job %s has already been deleted', jobNode)

                    if jobGraph2 != self:
                        logger.debug('Checkpoint is deleting old successor job: %s', jobGraph2.jobStoreID)
                        jobStore.delete(jobGraph2.jobStoreID)
                        successorsDeleted.append(jobGraph2.jobStoreID)

                recursiveDelete(self)
                self.stack = [[], []]
                self.services = []
                jobStore.update(self)
        return successorsDeleted

    def getLogFileHandle(self, jobStore):
        """
        Returns a context manager that yields a file handle to the log file
        """
        return jobStore.readFileStream(self.logJobStoreFileID)

    @classmethod
    def fromJobNode(cls, jobNode, jobStoreID, tryCount):
        """
        Builds a job graph from a given job node
        :param toil.job.JobNode jobNode: a job node object to build into a job graph
        :param str jobStoreID: the job store ID to assign to the resulting job graph object
        :param int tryCount: the number of times the resulting job graph object can be retried after
            failure
        :return: The newly created job graph object
        :rtype: toil.jobGraph.JobGraph
        """
        return cls(command=jobNode.command, jobStoreID=jobStoreID, 
         remainingRetryCount=tryCount, 
         predecessorNumber=jobNode.predecessorNumber, 
         unitName=jobNode.unitName, 
         jobName=jobNode.jobName, **jobNode._requirements)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.remainingRetryCount == other.remainingRetryCount and self.jobStoreID == other.jobStoreID and self.filesToDelete == other.filesToDelete and self.stack == other.stack and self.predecessorNumber == other.predecessorNumber and self.predecessorsFinished == other.predecessorsFinished and self.logJobStoreFileID == other.logJobStoreFileID