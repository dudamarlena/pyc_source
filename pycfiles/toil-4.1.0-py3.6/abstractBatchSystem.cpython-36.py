# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/abstractBatchSystem.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 24399 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from future.utils import with_metaclass
from builtins import object
import enum, os, shutil, logging
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from contextlib import contextmanager
from toil.lib.objects import abstractclassmethod
from toil.batchSystems import registry
from toil.common import Toil, cacheDirName
from toil.fileStores.abstractFileStore import AbstractFileStore
from toil.deferred import DeferredFunctionManager
try:
    from toil.cwl.cwltoil import CWL_INTERNAL_JOBS
except ImportError:
    CWL_INTERNAL_JOBS = ()

logger = logging.getLogger(__name__)
UpdatedBatchJobInfo = namedtuple('UpdatedBatchJobInfo', ('jobID', 'exitStatus', 'exitReason',
                                                         'wallTime'))

class BatchJobExitReason(enum.Enum):
    FINISHED = 1
    FAILED = 2
    LOST = 3
    KILLED = 4
    ERROR = 5


EXIT_STATUS_UNAVAILABLE_VALUE = 255
WorkerCleanupInfo = namedtuple('WorkerCleanupInfo', ('workDir', 'workflowID', 'cleanWorkDir'))

class AbstractBatchSystem(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    An abstract (as far as Python currently allows) base class to represent the interface the batch\n    system must provide to Toil.\n    '

    @abstractclassmethod
    def supportsAutoDeployment(cls):
        """
        Whether this batch system supports auto-deployment of the user script itself. If it does,
        the :meth:`.setUserScript` can be invoked to set the resource object representing the user
        script.

        Note to implementors: If your implementation returns True here, it should also override

        :rtype: bool
        """
        raise NotImplementedError()

    @abstractclassmethod
    def supportsWorkerCleanup(cls):
        """
        Indicates whether this batch system invokes :meth:`workerCleanup` after the last job for
        a particular workflow invocation finishes. Note that the term *worker* refers to an
        entire node, not just a worker process. A worker process may run more than one job
        sequentially, and more than one concurrent worker process may exist on a worker node,
        for the same workflow. The batch system is said to *shut down* after the last worker
        process terminates.

        :rtype: bool
        """
        raise NotImplementedError()

    def setUserScript(self, userScript):
        """
        Set the user script for this workflow. This method must be called before the first job is
        issued to this batch system, and only if :meth:`.supportsAutoDeployment` returns True,
        otherwise it will raise an exception.

        :param toil.resource.Resource userScript: the resource object representing the user script
               or module and the modules it depends on.
        """
        raise NotImplementedError()

    @abstractmethod
    def issueBatchJob(self, jobNode):
        """
        Issues a job with the specified command to the batch system and returns a unique jobID.

        :param jobNode a toil.job.JobNode

        :return: a unique jobID that can be used to reference the newly issued job
        :rtype: int
        """
        raise NotImplementedError()

    @abstractmethod
    def killBatchJobs(self, jobIDs):
        """
        Kills the given job IDs. After returning, the killed jobs will not
        appear in the results of getRunningBatchJobIDs. The killed job will not
        be returned from getUpdatedBatchJob.

        :param jobIDs: list of IDs of jobs to kill
        :type jobIDs: list[int]
        """
        raise NotImplementedError()

    @abstractmethod
    def getIssuedBatchJobIDs(self):
        """
        Gets all currently issued jobs

        :return: A list of jobs (as jobIDs) currently issued (may be running, or may be
                 waiting to be run). Despite the result being a list, the ordering should not
                 be depended upon.
        :rtype: list[str]
        """
        raise NotImplementedError()

    @abstractmethod
    def getRunningBatchJobIDs(self):
        """
        Gets a map of jobs as jobIDs that are currently running (not just waiting)
        and how long they have been running, in seconds.

        :return: dictionary with currently running jobID keys and how many seconds they have
                 been running as the value
        :rtype: dict[int,float]
        """
        raise NotImplementedError()

    @abstractmethod
    def getUpdatedBatchJob(self, maxWait):
        """
        Returns information about job that has updated its status (i.e. ceased
        running, either successfully or with an error). Each such job will be
        returned exactly once.
        
        Does not return info for jobs killed by killBatchJobs, although they
        may cause None to be returned earlier than maxWait.

        :param float maxWait: the number of seconds to block, waiting for a result

        :rtype: UpdatedBatchJobInfo or None
        :return: If a result is available, returns UpdatedBatchJobInfo.
                 Otherwise it returns None. wallTime is the number of seconds (a strictly 
                 positive float) in wall-clock time the job ran for, or None if this
                 batch system does not support tracking wall time.
        """
        raise NotImplementedError()

    def getSchedulingStatusMessage(self):
        """
        Get a log message fragment for the user about anything that might be
        going wrong in the batch system, if available.
        
        If no useful message is available, return None.
        
        This can be used to report what resource is the limiting factor when
        scheduling jobs, for example. If the leader thinks the workflow is
        stuck, the message can be displayed to the user to help them diagnose
        why it might be stuck.
        
        :rtype: str or None
        :return: User-directed message about scheduling state.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Called at the completion of a toil invocation.
        Should cleanly terminate all worker threads.
        """
        raise NotImplementedError()

    def setEnv(self, name, value=None):
        """
        Set an environment variable for the worker process before it is launched. The worker
        process will typically inherit the environment of the machine it is running on but this
        method makes it possible to override specific variables in that inherited environment
        before the worker is launched. Note that this mechanism is different to the one used by
        the worker internally to set up the environment of a job. A call to this method affects
        all jobs issued after this method returns. Note to implementors: This means that you
        would typically need to copy the variables before enqueuing a job.

        If no value is provided it will be looked up from the current environment.
        """
        raise NotImplementedError()

    @classmethod
    def setOptions(cls, setOption):
        """
        Process command line or configuration options relevant to this batch system.
        The

        :param setOption: A function with signature setOption(varName, parsingFn=None, checkFn=None, default=None)
           used to update run configuration
        """
        pass


class BatchSystemSupport(AbstractBatchSystem):
    __doc__ = '\n    Partial implementation of AbstractBatchSystem, support methods.\n    '

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(BatchSystemSupport, self).__init__()
        self.config = config
        self.maxCores = maxCores
        self.maxMemory = maxMemory
        self.maxDisk = maxDisk
        self.environment = {}
        self.workerCleanupInfo = WorkerCleanupInfo(workDir=(self.config.workDir), workflowID=(self.config.workflowID),
          cleanWorkDir=(self.config.cleanWorkDir))

    def checkResourceRequest(self, memory, cores, disk, name=None, detail=None):
        """
        Check resource request is not greater than that available or allowed.

        :param int memory: amount of memory being requested, in bytes

        :param float cores: number of cores being requested

        :param int disk: amount of disk space being requested, in bytes
        
        :param str name: Name of the job being checked, for generating a useful error report.
        
        :param str detail: Batch-system-specific message to include in the error.

        :raise InsufficientSystemResources: raised when a resource is requested in an amount
               greater than allowed
        """
        if not memory is not None:
            raise AssertionError
        else:
            if not disk is not None:
                raise AssertionError
            else:
                assert cores is not None
                if cores > self.maxCores:
                    raise InsufficientSystemResources('cores', cores, (self.maxCores), batchSystem=(self.__class__.__name__),
                      name=name,
                      detail=detail)
                if memory > self.maxMemory:
                    raise InsufficientSystemResources('memory', memory, (self.maxMemory), batchSystem=(self.__class__.__name__),
                      name=name,
                      detail=detail)
            if disk > self.maxDisk:
                raise InsufficientSystemResources('disk', disk, (self.maxDisk), batchSystem=(self.__class__.__name__),
                  name=name,
                  detail=detail)

    def setEnv(self, name, value=None):
        """
        Set an environment variable for the worker process before it is launched. The worker
        process will typically inherit the environment of the machine it is running on but this
        method makes it possible to override specific variables in that inherited environment
        before the worker is launched. Note that this mechanism is different to the one used by
        the worker internally to set up the environment of a job. A call to this method affects
        all jobs issued after this method returns. Note to implementors: This means that you
        would typically need to copy the variables before enqueuing a job.

        If no value is provided it will be looked up from the current environment.

        :param str name: the environment variable to be set on the worker.

        :param str value: if given, the environment variable given by name will be set to this value.
               if None, the variable's current value will be used as the value on the worker

        :raise RuntimeError: if value is None and the name cannot be found in the environment
        """
        if value is None:
            try:
                value = os.environ[name]
            except KeyError:
                raise RuntimeError('%s does not exist in current environment', name)

        self.environment[name] = value

    def formatStdOutErrPath(self, jobID, batchSystem, batchJobIDfmt, fileDesc):
        """
        Format path for batch system standard output/error and other files
        generated by the batch system itself.

        Files will be written to the Toil work directory (which may
        be on a shared file system) with names containing both the Toil and
        batch system job IDs, for ease of debugging job failures.

        :param: string jobID : Toil job ID
        :param: string batchSystem : Name of the batch system
        :param: string batchJobIDfmt : A string which the particular batch system
            will format into the batch job ID once it is submitted
        :param: string fileDesc : File description, should be 'std_output' for standard
             output, 'std_error' for standard error, and as appropriate for other files

        :rtype: string : Formatted filename; however if self.config.noStdOutErr is true,
             returns '/dev/null' or equivalent.

        """
        if self.config.noStdOutErr:
            return os.devnull
        else:
            workflowID = self.config.workflowID
            workDir = Toil.getToilWorkDir(self.config.workDir)
            fileName = 'toil_workflow_{workflowID}_job_{jobID}_batch_{batchSystem}_{batchJobIDfmt}_{fileDesc}.log'.format(workflowID=workflowID,
              jobID=jobID,
              batchSystem=batchSystem,
              batchJobIDfmt=batchJobIDfmt,
              fileDesc=fileDesc)
            return os.path.join(workDir, fileName)

    @staticmethod
    def workerCleanup(info):
        """
        Cleans up the worker node on batch system shutdown. Also see :meth:`supportsWorkerCleanup`.

        :param WorkerCleanupInfo info: A named tuple consisting of all the relevant information
               for cleaning up the worker.
        """
        assert isinstance(info, WorkerCleanupInfo)
        workflowDir = Toil.getLocalWorkflowDir(info.workflowID, info.workDir)
        DeferredFunctionManager.cleanupWorker(workflowDir)
        workflowDirContents = os.listdir(workflowDir)
        AbstractFileStore.shutdownFileStore(workflowDir, info.workflowID)
        if info.cleanWorkDir == 'always' or info.cleanWorkDir in ('onSuccess', 'onError') and workflowDirContents in ([], [cacheDirName(info.workflowID)]):
            shutil.rmtree(workflowDir, ignore_errors=True)


class BatchSystemLocalSupport(BatchSystemSupport):
    __doc__ = '\n    Adds a local queue for helper jobs, useful for CWL & others\n    '

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(BatchSystemLocalSupport, self).__init__(config, maxCores, maxMemory, maxDisk)
        self.localBatch = registry.batchSystemFactoryFor(registry.defaultBatchSystem())()(config, config.maxLocalJobs, maxMemory, maxDisk)

    def handleLocalJob(self, jobNode):
        """
        To be called by issueBatchJobs.

        Returns the jobID if the jobNode has been submitted to the local queue,
        otherwise returns None
        """
        if not self.config.runCwlInternalJobsOnWorkers:
            if jobNode.jobName.startswith(CWL_INTERNAL_JOBS):
                return self.localBatch.issueBatchJob(jobNode)
        return

    def killLocalJobs(self, jobIDs):
        """
        To be called by killBatchJobs. Will kill all local jobs that match the
        provided jobIDs.
        """
        self.localBatch.killBatchJobs(jobIDs)

    def getIssuedLocalJobIDs(self):
        """To be called by getIssuedBatchJobIDs"""
        return self.localBatch.getIssuedBatchJobIDs()

    def getRunningLocalJobIDs(self):
        """To be called by getRunningBatchJobIDs()."""
        return self.localBatch.getRunningBatchJobIDs()

    def getUpdatedLocalJob(self, maxWait):
        """To be called by getUpdatedBatchJob()"""
        return self.localBatch.getUpdatedBatchJob(maxWait)

    def getNextJobID(self):
        """
        Must be used to get job IDs so that the local and batch jobs do not
        conflict.
        """
        with self.localBatch.jobIndexLock:
            jobID = self.localBatch.jobIndex
            self.localBatch.jobIndex += 1
        return jobID

    def shutdownLocal(self):
        """To be called from shutdown()"""
        self.localBatch.shutdown()


class NodeInfo(object):
    __doc__ = "\n    The coresUsed attribute  is a floating point value between 0 (all cores idle) and 1 (all cores\n    busy), reflecting the CPU load of the node.\n\n    The memoryUsed attribute is a floating point value between 0 (no memory used) and 1 (all memory\n    used), reflecting the memory pressure on the node.\n\n    The coresTotal and memoryTotal attributes are the node's resources, not just the used resources\n\n    The requestedCores and requestedMemory attributes are all the resources that Toil Jobs have reserved on the\n    node, regardless of whether the resources are actually being used by the Jobs.\n\n    The workers attribute is an integer reflecting the number of workers currently active workers\n    on the node.\n    "

    def __init__(self, coresUsed, memoryUsed, coresTotal, memoryTotal, requestedCores, requestedMemory, workers):
        self.coresUsed = coresUsed
        self.memoryUsed = memoryUsed
        self.coresTotal = coresTotal
        self.memoryTotal = memoryTotal
        self.requestedCores = requestedCores
        self.requestedMemory = requestedMemory
        self.workers = workers


class AbstractScalableBatchSystem(AbstractBatchSystem):
    __doc__ = '\n    A batch system that supports a variable number of worker nodes. Used by :class:`toil.\n    provisioners.clusterScaler.ClusterScaler` to scale the number of worker nodes in the cluster\n    up or down depending on overall load.\n    '

    @abstractmethod
    def getNodes(self, preemptable=None):
        """
        Returns a dictionary mapping node identifiers of preemptable or non-preemptable nodes to
        NodeInfo objects, one for each node.

        :param bool preemptable: If True (False) only (non-)preemptable nodes will be returned.
               If None, all nodes will be returned.

        :rtype: dict[str,NodeInfo]
        """
        raise NotImplementedError()

    @abstractmethod
    def nodeInUse(self, nodeIP):
        """
        Can be used to determine if a worker node is running any tasks. If the node is doesn't
        exist, this function should simply return False.

        :param str nodeIP: The worker nodes private IP address

        :return: True if the worker node has been issued any tasks, else False
        :rtype: bool
        """
        raise NotImplementedError()

    @abstractmethod
    @contextmanager
    def nodeFiltering(self, filter):
        """
        Used to prevent races in autoscaling where
        1) nodes have reported to the autoscaler as having no jobs
        2) scaler decides to terminate these nodes. In parallel the batch system assigns jobs to the same nodes
        3) scaler terminates nodes, resulting in job failures for all jobs on that node.

        Call this method prior to node termination to ensure that nodes being considered for termination are not
        assigned new jobs. Call the method again passing None as the filter to disable the filtering
        after node termination is done.

        :param method: This will be used as a filter on nodes considered when assigning new jobs.
            After this context manager exits the filter should be removed
        :rtype: None
        """
        raise NotImplementedError()

    @abstractmethod
    def ignoreNode(self, nodeAddress):
        """
        Stop sending jobs to this node. Used in autoscaling
        when the autoscaler is ready to terminate a node, but
        jobs are still running. This allows the node to be terminated
        after the current jobs have finished.

        :param str: IP address of node to ignore.
        :rtype: None
        """
        raise NotImplementedError()

    @abstractmethod
    def unignoreNode(self, nodeAddress):
        """
        Stop ignoring this address, presumably after
        a node with this address has been terminated. This allows for the
        possibility of a new node having the same address as a terminated one.
        """
        raise NotImplementedError()


class InsufficientSystemResources(Exception):
    __doc__ = '\n    To be raised when a job requests more of a particular resource than is either currently allowed\n    or avaliable\n    '

    def __init__(self, resource, requested, available, batchSystem=None, name=None, detail=None):
        """
        Creates an instance of this exception that indicates which resource is insufficient for current
        demands, as well as the amount requested and amount actually available.

        :param str resource: string representing the resource type

        :param int|float requested: the amount of the particular resource requested that resulted
               in this exception

        :param int|float available: amount of the particular resource actually available
        
        :param str batchSystem: Name of the batch system class complaining, for
                   generating a useful error report. If you are using a single machine
                   batch system for local jobs in another batch system, it is important to
                   know which one has run out of resources.
        
        :param str name: Name of the job being checked, for generating a useful error report.
        
        :param str detail: Batch-system-specific message to include in the error.
        """
        self.requested = requested
        self.available = available
        self.resource = resource
        self.batchSystem = batchSystem if batchSystem is not None else 'this batch system'
        self.unit = 'bytes of ' if resource == 'disk' or resource == 'memory' else ''
        self.name = name
        self.detail = detail

    def __str__(self):
        if self.name is not None:
            phrases = [
             'The job {} is requesting {} {}{}, more than the maximum of {} {}{} that {} was configured with.'.format(self.name, self.requested, self.unit, self.resource, self.available, self.unit, self.resource, self.batchSystem)]
        else:
            phrases = [
             'Requesting more {} than either physically available to {}, or enforced by --max{}. Requested: {}, Available: {}'.format(self.resource, self.batchSystem, self.resource.capitalize(), self.requested, self.available)]
        if self.detail is not None:
            phrases.append(self.detail)
        return ' '.join(phrases)