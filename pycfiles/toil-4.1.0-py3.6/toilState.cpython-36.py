# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/toilState.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 8266 bytes
from __future__ import absolute_import
from builtins import object
import logging
logger = logging.getLogger(__name__)

class ToilState(object):
    __doc__ = '\n    Represents a snapshot of the jobs in the jobStore. Used by the leader to manage the batch.\n    '

    def __init__(self, jobStore, rootJob, jobCache=None):
        """
        Loads the state from the jobStore, using the rootJob 
        as the source of the job graph.

        The jobCache is a map from jobStoreIDs to jobGraphs or None. Is used to
        speed up the building of the state.

        :param toil.jobStores.abstractJobStore.AbstractJobStore jobStore 
        :param toil.jobWrapper.JobGraph rootJob
        """
        self.successorJobStoreIDToPredecessorJobs = {}
        self.successorCounts = {}
        self.serviceJobStoreIDToPredecessorJob = {}
        self.servicesIssued = {}
        self.updatedJobs = set()
        self.totalFailedJobs = set()
        self.hasFailedSuccessors = set()
        self.failedSuccessors = set()
        self.jobsToBeScheduledWithMultiplePredecessors = {}
        self._buildToilState(rootJob, jobStore, jobCache)

    def _buildToilState(self, jobGraph, jobStore, jobCache=None):
        """
        Traverses tree of jobs from the root jobGraph (rootJob) building the
        ToilState class.

        If jobCache is passed, it must be a dict from job ID to JobGraph
        object. Jobs will be loaded from the cache (which can be downloaded from
        the jobStore in a batch) instead of piecemeal when recursed into.

        :param jobGraph: Object representing a job.
        :param jobStore: Object inheriting toil.jobStores.abstractJobStore.AbstractJobStore.
        :param jobCache:
        :return:
        """

        def getJob(jobId):
            if jobCache is not None:
                if jobId in jobCache:
                    return jobCache[jobId]
            return jobStore.load(jobId)

        if jobGraph.command is not None or jobGraph.checkpoint is not None or jobGraph.services or not jobGraph.stack:
            logger.debug('Found job to run: %s, with command: %s, with checkpoint: %s, with  services: %s, with stack: %s', jobGraph.jobStoreID, jobGraph.command is not None, jobGraph.checkpoint is not None, len(jobGraph.services) > 0, len(jobGraph.stack) == 0)
            self.updatedJobs.add((jobGraph, 0))
            if jobGraph.checkpoint is not None:
                jobGraph.command = jobGraph.checkpoint
        else:
            logger.debug('Adding job: %s to the state with %s successors' % (jobGraph.jobStoreID, len(jobGraph.stack[(-1)])))
            self.successorCounts[jobGraph.jobStoreID] = len(jobGraph.stack[(-1)])

            def processSuccessorWithMultiplePredecessors(successorJobGraph):
                if jobGraph.jobStoreID not in successorJobGraph.predecessorsFinished:
                    successorJobGraph.predecessorsFinished.add(jobGraph.jobStoreID)
                else:
                    assert len(successorJobGraph.predecessorsFinished) <= successorJobGraph.predecessorNumber
                    if len(successorJobGraph.predecessorsFinished) == successorJobGraph.predecessorNumber:
                        self.jobsToBeScheduledWithMultiplePredecessors.pop(successorJobStoreID)
                        self._buildToilState(successorJobGraph, jobStore, jobCache=jobCache)

            for successorJobNode in jobGraph.stack[(-1)]:
                successorJobStoreID = successorJobNode.jobStoreID
                if successorJobStoreID not in self.successorJobStoreIDToPredecessorJobs:
                    self.successorJobStoreIDToPredecessorJobs[successorJobStoreID] = [
                     jobGraph]
                    if successorJobNode.predecessorNumber > 1:
                        successorJobGraph = getJob(successorJobStoreID)
                        assert successorJobStoreID not in self.jobsToBeScheduledWithMultiplePredecessors
                        self.jobsToBeScheduledWithMultiplePredecessors[successorJobStoreID] = successorJobGraph
                        processSuccessorWithMultiplePredecessors(successorJobGraph)
                    else:
                        self._buildToilState((getJob(successorJobStoreID)), jobStore, jobCache=jobCache)
                else:
                    assert jobGraph not in self.successorJobStoreIDToPredecessorJobs[successorJobStoreID]
                    self.successorJobStoreIDToPredecessorJobs[successorJobStoreID].append(jobGraph)
                    if successorJobStoreID in self.jobsToBeScheduledWithMultiplePredecessors:
                        successorJobGraph = self.jobsToBeScheduledWithMultiplePredecessors[successorJobStoreID]
                        processSuccessorWithMultiplePredecessors(successorJobGraph)