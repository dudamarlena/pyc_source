# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/mesos/batchSystem.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 38060 bytes
from __future__ import absolute_import
from builtins import filter
from builtins import str
from builtins import object
import ast, logging, os, pwd, socket, time, sys, getpass, json, traceback, addict, subprocess
try:
    from urllib2 import urlopen
    from urllib import quote_plus
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote_plus

from contextlib import contextmanager
from six.moves.queue import Empty, Queue
from six import iteritems, itervalues
from pymesos import MesosSchedulerDriver, Scheduler, encode_data, decode_data
from toil.lib.compatibility import USING_PYTHON2
from toil import pickle
from toil.lib.memoize import strict_bool
from toil import resolveEntryPoint
from toil.batchSystems.abstractBatchSystem import AbstractScalableBatchSystem, BatchJobExitReason, BatchSystemLocalSupport, EXIT_STATUS_UNAVAILABLE_VALUE, NodeInfo, UpdatedBatchJobInfo
from toil.batchSystems.mesos import ToilJob, MesosShape, TaskData, JobQueue
log = logging.getLogger(__name__)

class MesosBatchSystem(BatchSystemLocalSupport, AbstractScalableBatchSystem, Scheduler):
    __doc__ = '\n    A Toil batch system implementation that uses Apache Mesos to distribute toil jobs as Mesos\n    tasks over a cluster of agent nodes. A Mesos framework consists of a scheduler and an\n    executor. This class acts as the scheduler and is typically run on the master node that also\n    runs the Mesos master process with which the scheduler communicates via a driver component.\n    The executor is implemented in a separate class. It is run on each agent node and\n    communicates with the Mesos agent process via another driver object. The scheduler may also\n    be run on a separate node from the master, which we then call somewhat ambiguously the driver\n    node.\n    '

    @classmethod
    def supportsAutoDeployment(cls):
        return True

    @classmethod
    def supportsWorkerCleanup(cls):
        return True

    class ExecutorInfo(object):

        def __init__(self, nodeAddress, agentId, nodeInfo, lastSeen):
            super(MesosBatchSystem.ExecutorInfo, self).__init__()
            self.nodeAddress = nodeAddress
            self.agentId = agentId
            self.nodeInfo = nodeInfo
            self.lastSeen = lastSeen

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(MesosBatchSystem, self).__init__(config, maxCores, maxMemory, maxDisk)
        self.userScript = None
        self.jobQueues = JobQueue()
        self.mesosMasterAddress = config.mesosMasterAddress
        self.killedJobIds = set()
        self.killJobIds = set()
        self.intendedKill = set()
        self.hostToJobIDs = {}
        self.nodeFilter = []
        self.runningJobMap = {}
        self.taskResources = {}
        self.updatedJobsQueue = Queue()
        self.driver = None
        self.frameworkId = None
        self.executors = {}
        self.agentsByID = {}
        self.nonPreemptableNodes = set()
        self.executor = self._buildExecutor()
        self.lastTimeOfferLogged = 0
        self.logPeriod = 30
        self.ignoredNodes = set()
        self._startDriver()

    def setUserScript(self, userScript):
        self.userScript = userScript

    def ignoreNode(self, nodeAddress):
        self.ignoredNodes.add(nodeAddress)

    def unignoreNode(self, nodeAddress):
        self.ignoredNodes.remove(nodeAddress)

    def issueBatchJob(self, jobNode):
        """
        Issues the following command returning a unique jobID. Command is the string to run, memory
        is an int giving the number of bytes the job needs to run in and cores is the number of cpus
        needed for the job and error-file is the path of the file to place any std-err/std-out in.
        """
        localID = self.handleLocalJob(jobNode)
        if localID:
            return localID
        else:
            self.checkResourceRequest(jobNode.memory, jobNode.cores, jobNode.disk)
            jobID = self.getNextJobID()
            job = ToilJob(jobID=jobID, name=(str(jobNode)),
              resources=MesosShape(wallTime=0, **jobNode._requirements),
              command=(jobNode.command),
              userScript=(self.userScript),
              environment=(self.environment.copy()),
              workerCleanupInfo=(self.workerCleanupInfo))
            jobType = job.resources
            log.debug('Queueing the job command: %s with job id: %s ...', jobNode.command, str(jobID))
            self.taskResources[jobID] = job.resources
            self.jobQueues.insertJob(job, jobType)
            log.debug('... queued')
            return jobID

    def killBatchJobs(self, jobIDs):
        self.killLocalJobs(jobIDs)
        assert self.driver is not None
        localSet = set()
        for jobID in jobIDs:
            self.killJobIds.add(jobID)
            localSet.add(jobID)
            self.intendedKill.add(jobID)
            if jobID in self.getIssuedBatchJobIDs():
                taskId = addict.Dict()
                taskId.value = str(jobID)
                log.debug('Kill issued job %s' % str(jobID))
                self.driver.killTask(taskId)
            else:
                log.debug('Skip non-issued job %s' % str(jobID))
                self.killJobIds.remove(jobID)
                localSet.remove(jobID)

        while localSet:
            intersection = localSet.intersection(self.killedJobIds)
            if intersection:
                localSet -= intersection
                self.killedJobIds -= intersection
            else:
                time.sleep(1)

    def getIssuedBatchJobIDs(self):
        jobIds = set(self.jobQueues.jobIDs())
        jobIds.update(list(self.runningJobMap.keys()))
        return list(jobIds) + list(self.getIssuedLocalJobIDs())

    def getRunningBatchJobIDs(self):
        currentTime = dict()
        for jobID, data in list(self.runningJobMap.items()):
            currentTime[jobID] = time.time() - data.startTime

        currentTime.update(self.getRunningLocalJobIDs())
        return currentTime

    def getUpdatedBatchJob(self, maxWait):
        local_tuple = self.getUpdatedLocalJob(0)
        if local_tuple:
            return local_tuple
        while True:
            try:
                item = self.updatedJobsQueue.get(timeout=maxWait)
            except Empty:
                return
            else:
                try:
                    self.intendedKill.remove(item.jobID)
                except KeyError:
                    log.debug('Job %s ended with status %i, took %s seconds.', item.jobID, item.exitStatus, '???' if item.wallTime is None else str(item.wallTime))
                    return item
                else:
                    log.debug('Job %s ended naturally before it could be killed.', item.jobID)

    def nodeInUse(self, nodeIP):
        return nodeIP in self.hostToJobIDs

    @contextmanager
    def nodeFiltering(self, filter):
        self.nodeFilter = [filter]
        yield
        self.nodeFilter = []

    def getWaitDuration(self):
        """
        Gets the period of time to wait (floating point, in seconds) between checking for
        missing/overlong jobs.
        """
        return 1

    def _buildExecutor(self):
        """
        Creates and returns an ExecutorInfo-shaped object representing our executor implementation.
        """
        info = addict.Dict()
        info.name = 'toil'
        info.command.value = resolveEntryPoint('_toil_mesos_executor')
        info.executor_id.value = 'toil-%i' % os.getpid()
        info.source = pwd.getpwuid(os.getuid()).pw_name
        return info

    def _startDriver(self):
        """
        The Mesos driver thread which handles the scheduler's communication with the Mesos master
        """
        framework = addict.Dict()
        framework.user = getpass.getuser()
        framework.name = 'toil'
        framework.principal = framework.name
        self.driver = MesosSchedulerDriver(self, framework, (self._resolveAddress(self.mesosMasterAddress)),
          use_addict=True,
          implicit_acknowledgements=True)
        self.driver.start()

    @staticmethod
    def _resolveAddress(address):
        """
        Resolves the host in the given string. The input is of the form host[:port]. This method
        is idempotent, i.e. the host may already be a dotted IP address.

        >>> # noinspection PyProtectedMember
        >>> f=MesosBatchSystem._resolveAddress
        >>> f('localhost')
        '127.0.0.1'
        >>> f('127.0.0.1')
        '127.0.0.1'
        >>> f('localhost:123')
        '127.0.0.1:123'
        >>> f('127.0.0.1:123')
        '127.0.0.1:123'
        """
        address = address.split(':')
        assert len(address) in (1, 2)
        address[0] = socket.gethostbyname(address[0])
        return ':'.join(address)

    def shutdown(self):
        self.shutdownLocal()
        log.debug('Stopping Mesos driver')
        self.driver.stop()
        log.debug('Joining Mesos driver')
        driver_result = self.driver.join()
        log.debug('Joined Mesos driver')
        if driver_result is not None:
            if driver_result != 'DRIVER_STOPPED':
                raise RuntimeError('Mesos driver failed with %s' % driver_result)

    def registered(self, driver, frameworkId, masterInfo):
        """
        Invoked when the scheduler successfully registers with a Mesos master
        """
        log.debug('Registered with framework ID %s', frameworkId.value)
        self.frameworkId = frameworkId.value

    def _declineAllOffers(self, driver, offers):
        for offer in offers:
            log.debug('Declining offer %s.', offer.id.value)
            driver.declineOffer(offer.id)

    def _parseOffer(self, offer):
        cores = 0
        memory = 0
        disk = 0
        preemptable = None
        for attribute in offer.attributes:
            if attribute.name == 'preemptable':
                assert preemptable is None, "Attribute 'preemptable' occurs more than once."
                preemptable = strict_bool(attribute.text.value)

        if preemptable is None:
            log.debug('Agent not marked as either preemptable or not. Assuming non-preemptable.')
            preemptable = False
        for resource in offer.resources:
            if resource.name == 'cpus':
                cores += resource.scalar.value
            else:
                if resource.name == 'mem':
                    memory += resource.scalar.value
                else:
                    if resource.name == 'disk':
                        disk += resource.scalar.value

        return (
         cores, memory, disk, preemptable)

    def _prepareToRun(self, jobType, offer):
        job = self.jobQueues.nextJobOfType(jobType)
        task = self._newMesosTask(job, offer)
        return task

    def _updateStateToRunning(self, offer, runnableTasks):
        for task in runnableTasks:
            resourceKey = int(task.task_id.value)
            resources = self.taskResources[resourceKey]
            agentIP = socket.gethostbyname(offer.hostname)
            try:
                self.hostToJobIDs[agentIP].append(resourceKey)
            except KeyError:
                self.hostToJobIDs[agentIP] = [
                 resourceKey]

            self.runningJobMap[int(task.task_id.value)] = TaskData(startTime=(time.time()), agentID=(offer.agent_id.value),
              agentIP=agentIP,
              executorID=(task.executor.executor_id.value),
              cores=(resources.cores),
              memory=(resources.memory))
            del self.taskResources[resourceKey]
            log.debug('Launched Mesos task %s.', task.task_id.value)

    def resourceOffers(self, driver, offers):
        """
        Invoked when resources have been offered to this framework.
        """
        self._trackOfferedNodes(offers)
        jobTypes = self.jobQueues.sortedTypes
        if not jobTypes:
            log.debug('There are no queued tasks. Declining Mesos offers.')
            self._declineAllOffers(driver, offers)
            return
        unableToRun = True
        for offer in offers:
            if offer.hostname in self.ignoredNodes:
                log.debug('Declining offer %s because node %s is designated for termination' % (
                 offer.id.value, offer.hostname))
                driver.declineOffer(offer.id)
            else:
                runnableTasks = []
                offerCores, offerMemory, offerDisk, offerPreemptable = self._parseOffer(offer)
                log.debug('Got offer %s for a %spreemptable agent with %.2f MiB memory, %.2f core(s) and %.2f MiB of disk.', offer.id.value, '' if offerPreemptable else 'non-', offerMemory, offerCores, offerDisk)
                remainingCores = offerCores
                remainingMemory = offerMemory
                remainingDisk = offerDisk
                for jobType in jobTypes:
                    runnableTasksOfType = []
                    nextToLaunchIndex = 0
                    while not self.jobQueues.typeEmpty(jobType) and (not offerPreemptable or jobType.preemptable) and remainingCores >= jobType.cores and remainingDisk >= toMiB(jobType.disk) and remainingMemory >= toMiB(jobType.memory):
                        task = self._prepareToRun(jobType, offer)
                        assert int(task.task_id.value) not in self.runningJobMap
                        runnableTasksOfType.append(task)
                        log.debug('Preparing to launch Mesos task %s with %.2f cores, %.2f MiB memory, and %.2f MiB disk using offer %s ...', task.task_id.value, jobType.cores, toMiB(jobType.memory), toMiB(jobType.disk), offer.id.value)
                        remainingCores -= jobType.cores
                        remainingMemory -= toMiB(jobType.memory)
                        remainingDisk -= toMiB(jobType.disk)
                        nextToLaunchIndex += 1

                    if not self.jobQueues.typeEmpty(jobType):
                        log.debug('Offer %(offer)s not suitable to run the tasks with requirements %(requirements)r. Mesos offered %(memory)s memory, %(cores)s cores and %(disk)s of disk on a %(non)spreemptable agent.', dict(offer=(offer.id.value), requirements=(jobType.__dict__),
                          non=('' if offerPreemptable else 'non-'),
                          memory=(fromMiB(offerMemory)),
                          cores=offerCores,
                          disk=(fromMiB(offerDisk))))
                    runnableTasks.extend(runnableTasksOfType)

                if runnableTasks:
                    unableToRun = False
                    driver.launchTasks(offer.id, runnableTasks)
                    self._updateStateToRunning(offer, runnableTasks)
                else:
                    log.debug('Although there are queued jobs, none of them could be run with offer %s extended to the framework.', offer.id)
                    driver.declineOffer(offer.id)

        if unableToRun:
            if time.time() > self.lastTimeOfferLogged + self.logPeriod:
                self.lastTimeOfferLogged = time.time()
                log.debug('Although there are queued jobs, none of them were able to run in any of the offers extended to the framework. There are currently %i jobs running. Enable debug level logging to see more details about job types and offers received.', len(self.runningJobMap))

    def _trackOfferedNodes(self, offers):
        for offer in offers:
            assert 'value' in offer.agent_id
            try:
                nodeAddress = socket.gethostbyname(offer.hostname)
            except:
                log.debug('Failed to resolve hostname %s' % offer.hostname)
                raise

            self._registerNode(nodeAddress, offer.agent_id.value)
            preemptable = False
            for attribute in offer.attributes:
                if attribute.name == 'preemptable':
                    preemptable = strict_bool(attribute.text.value)

            if preemptable:
                try:
                    self.nonPreemptableNodes.remove(offer.agent_id.value)
                except KeyError:
                    pass

            else:
                self.nonPreemptableNodes.add(offer.agent_id.value)

    def _filterOfferedNodes(self, offers):
        if not self.nodeFilter:
            return offers
        else:
            executorInfoOrNone = [self.executors.get(socket.gethostbyname(offer.hostname)) for offer in offers]
            executorInfos = [_f for _f in executorInfoOrNone if _f]
            executorsToConsider = list(filter(self.nodeFilter[0], executorInfos))
            ipsToConsider = {ex.nodeAddress for ex in executorsToConsider}
            return [offer for offer in offers if socket.gethostbyname(offer.hostname) in ipsToConsider]

    def _newMesosTask(self, job, offer):
        """
        Build the Mesos task object for a given the Toil job and Mesos offer
        """
        task = addict.Dict()
        task.task_id.value = str(job.jobID)
        task.agent_id.value = offer.agent_id.value
        task.name = job.name
        task.data = encode_data(pickle.dumps(job))
        task.executor = addict.Dict(self.executor)
        task.resources = []
        task.resources.append(addict.Dict())
        cpus = task.resources[(-1)]
        cpus.name = 'cpus'
        cpus.type = 'SCALAR'
        cpus.scalar.value = job.resources.cores
        task.resources.append(addict.Dict())
        disk = task.resources[(-1)]
        disk.name = 'disk'
        disk.type = 'SCALAR'
        if toMiB(job.resources.disk) > 1:
            disk.scalar.value = toMiB(job.resources.disk)
        else:
            log.warning('Job %s uses less disk than Mesos requires. Rounding %s up to 1 MiB.', job.jobID, job.resources.disk)
            disk.scalar.value = 1
        task.resources.append(addict.Dict())
        mem = task.resources[(-1)]
        mem.name = 'mem'
        mem.type = 'SCALAR'
        if toMiB(job.resources.memory) > 1:
            mem.scalar.value = toMiB(job.resources.memory)
        else:
            log.warning('Job %s uses less memory than Mesos requires. Rounding %s up to 1 MiB.', job.jobID, job.resources.memory)
            mem.scalar.value = 1
        return task

    def statusUpdate(self, driver, update):
        """
        Invoked when the status of a task has changed (e.g., a agent is lost and so the task is
        lost, a task finishes and an executor sends a status update saying so, etc). Note that
        returning from this callback _acknowledges_ receipt of this status update! If for
        whatever reason the scheduler aborts during this callback (or the process exits) another
        status update will be delivered (note, however, that this is currently not true if the
        agent sending the status update is lost/fails during that time).
        """
        jobID = int(update.task_id.value)
        log.debug("Job %i is in state '%s' due to reason '%s'.", jobID, update.state, update.reason)

        def jobEnded(_exitStatus, wallTime=None, exitReason=None):
            """
            Notify external observers of the job ending.
            """
            self.updatedJobsQueue.put(UpdatedBatchJobInfo(jobID=jobID, exitStatus=_exitStatus, wallTime=wallTime, exitReason=exitReason))
            agentIP = None
            try:
                agentIP = self.runningJobMap[jobID].agentIP
            except KeyError:
                log.warning("Job %i returned exit code %i but isn't tracked as running.", jobID, _exitStatus)
            else:
                del self.runningJobMap[jobID]
            try:
                self.hostToJobIDs[agentIP].remove(jobID)
            except KeyError:
                log.warning('Job %i returned exit code %i from unknown host.', jobID, _exitStatus)

            try:
                self.killJobIds.remove(jobID)
            except KeyError:
                pass
            else:
                self.killedJobIds.add(jobID)

        if update.state == 'TASK_FINISHED':
            labels = update.labels.labels
            wallTime = None
            for label in labels:
                if label['key'] == 'wallTime':
                    wallTime = float(label['value'])
                    break

            assert wallTime is not None
            jobEnded(0, wallTime=wallTime, exitReason=(BatchJobExitReason.FINISHED))
        else:
            if update.state == 'TASK_FAILED':
                try:
                    exitStatus = int(update.message)
                except ValueError:
                    exitStatus = EXIT_STATUS_UNAVAILABLE_VALUE
                    log.warning("Job %i failed with message '%s' due to reason '%s' on executor '%s' on agent '%s'.", jobID, update.message, update.reason, update.executor_id, update.agent_id)
                else:
                    log.warning("Job %i failed with exit status %i and message '%s' due to reason '%s' on executor '%s' on agent '%s'.", jobID, exitStatus, update.message, update.reason, update.executor_id, update.agent_id)
                jobEnded(exitStatus, exitReason=(BatchJobExitReason.FAILED))
            else:
                if update.state == 'TASK_LOST':
                    log.warning('Job %i is lost.', jobID)
                    jobEnded(EXIT_STATUS_UNAVAILABLE_VALUE, exitReason=(BatchJobExitReason.LOST))
                else:
                    if update.state in ('TASK_KILLED', 'TASK_ERROR'):
                        log.warning("Job %i is in unexpected state %s with message '%s' due to reason '%s'.", jobID, update.state, update.message, update.reason)
                        jobEnded(EXIT_STATUS_UNAVAILABLE_VALUE, exitReason=(BatchJobExitReason.KILLED if update.state == 'TASK_KILLED' else BatchJobExitReason.ERROR))
        if 'limitation' in update:
            log.warning('Job limit info: %s' % update.limitation)

    def frameworkMessage(self, driver, executorId, agentId, message):
        """
        Invoked when an executor sends a message.
        """
        if USING_PYTHON2:
            message = decode_data(message)
        else:
            message = decode_data(message).decode()
        log.debug('Got framework message from executor %s running on agent %s: %s', executorId.value, agentId.value, message)
        message = ast.literal_eval(message)
        assert isinstance(message, dict)
        nodeAddress = message.pop('address')
        executor = self._registerNode(nodeAddress, agentId.value)
        for k, v in iteritems(message):
            if k == 'nodeInfo':
                assert isinstance(v, dict)
                resources = [taskData for taskData in itervalues(self.runningJobMap) if taskData.executorID == executorId.value]
                requestedCores = sum(taskData.cores for taskData in resources)
                requestedMemory = sum(taskData.memory for taskData in resources)
                executor.nodeInfo = NodeInfo(requestedCores=requestedCores, requestedMemory=requestedMemory, **v)
                self.executors[nodeAddress] = executor
            else:
                raise RuntimeError("Unknown message field '%s'." % k)

    def _registerNode(self, nodeAddress, agentId, nodePort=5051):
        """
        Called when we get communication from an agent. Remembers the
        information about the agent by address, and the agent address by agent
        ID.
        """
        executor = self.executors.get(nodeAddress)
        if executor is None or executor.agentId != agentId:
            executor = self.ExecutorInfo(nodeAddress=nodeAddress, agentId=agentId,
              nodeInfo=None,
              lastSeen=(time.time()))
            self.executors[nodeAddress] = executor
        else:
            executor.lastSeen = time.time()
        self.agentsByID[agentId] = nodeAddress
        return executor

    def getNodes(self, preemptable=None, timeout=600):
        timeout = timeout or sys.maxsize
        return {nodeAddress:executor.nodeInfo for nodeAddress, executor in iteritems(self.executors) if preemptable is None or preemptable == (executor.agentId not in self.nonPreemptableNodes)}

    def reregistered(self, driver, masterInfo):
        """
        Invoked when the scheduler re-registers with a newly elected Mesos master.
        """
        log.debug('Registered with new master')

    def _handleFailedExecutor(self, agentID, executorID=None):
        """
        Should be called when we find out an executor has failed.
        
        Gets the log from some container (since we are never handed a container
        ID) that ran on the given executor on the given agent, if the agent is
        still up, and dumps it to our log. All IDs are strings.
        
        If executorID is None, dumps all executors from the agent.
        
        Useful for debugging failing executor code.
        """
        log.warning("Handling failure of executor '%s' on agent '%s'.", executorID, agentID)
        try:
            agentAddress = self.agentsByID[agentID]
            agentPort = 5051
            filesQueryURL = errorLogURL = 'http://%s:%d/files/debug' % (
             agentAddress, agentPort)
            filesDict = json.loads(urlopen(filesQueryURL).read())
            log.debug('Available files: %s', repr(filesDict.keys()))
            stderrFilenames = []
            agentLogFilenames = []
            for filename in filesDict.iterkeys():
                if self.frameworkId in filename and agentID in filename and (executorID is None or executorID in filename):
                    stderrFilenames.append('%s/stderr' % filename)
                else:
                    if filename.endswith('log'):
                        agentLogFilenames.append(filename)

            if '/slave/log' not in agentLogFilenames:
                agentLogFilenames.append('/slave/log')
            if len(stderrFilenames) == 0:
                log.warning("Could not find any containers in '%s'." % filesDict)
            for stderrFilename in stderrFilenames:
                try:
                    errorLogURL = 'http://%s:%d/files/download?path=%s' % (
                     agentAddress, agentPort, quote_plus(stderrFilename))
                    log.warning('Attempting to retrieve executor error log: %s', errorLogURL)
                    for line in urlopen(errorLogURL):
                        log.warning('Executor: %s', line.rstrip())

                except Exception as e:
                    log.warning("Could not retrieve exceutor log due to: '%s'.", e)
                    log.warning(traceback.format_exc())

            for agentLogFilename in agentLogFilenames:
                try:
                    agentLogURL = 'http://%s:%d/files/download?path=%s' % (
                     agentAddress, agentPort, quote_plus(agentLogFilename))
                    log.warning('Attempting to retrieve agent log: %s', agentLogURL)
                    for line in urlopen(agentLogURL):
                        log.warning('Agent: %s', line.rstrip())

                except Exception as e:
                    log.warning("Could not retrieve agent log due to: '%s'.", e)
                    log.warning(traceback.format_exc())

        except Exception as e:
            log.warning("Could not retrieve logs due to: '%s'.", e)
            log.warning(traceback.format_exc())

    def executorLost(self, driver, executorId, agentId, status):
        """
        Invoked when an executor has exited/terminated abnormally.
        """
        failedId = executorId.get('value', None)
        log.warning("Executor '%s' reported lost with status '%s'.", failedId, status)
        self._handleFailedExecutor(agentId.value, failedId)

    @classmethod
    def setOptions(cls, setOption):
        setOption('mesosMasterAddress', None, None, 'localhost:5050')


def toMiB(n):
    return n / 1024 / 1024


def fromMiB(n):
    return n * 1024 * 1024