# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/provisioners/clusterScaler.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 48472 bytes
from __future__ import absolute_import
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import map
from builtins import object
import json, logging, os, time
from collections import defaultdict
from toil.lib.retry import retry
from toil.lib.threading import ExceptionalThread
from toil.lib.throttle import throttle
from itertools import islice
from toil.batchSystems.abstractBatchSystem import AbstractScalableBatchSystem, NodeInfo
from toil.provisioners.abstractProvisioner import Shape
from toil.job import ServiceJobNode
from toil.common import defaultTargetTime
logger = logging.getLogger(__name__)

class BinPackedFit(object):
    __doc__ = '\n    If jobShapes is a set of tasks with run requirements (mem/disk/cpu), and nodeShapes is a sorted\n    list of available computers to run these jobs on, this function attempts to return a dictionary\n    representing the minimum set of computerNode computers needed to run the tasks in jobShapes.\n\n    Uses a first fit decreasing (FFD) bin packing like algorithm to calculate an approximate minimum\n    number of nodes that will fit the given list of jobs.  BinPackingFit assumes the ordered list,\n    nodeShapes, is ordered for "node preference" outside of BinPackingFit beforehand. So when\n    virtually "creating" nodes, the first node within nodeShapes that fits the job is the one\n    that\'s added.\n\n    :param list nodeShapes: The properties of an atomic node allocation, in terms of wall-time,\n                            memory, cores, disk, and whether it is preemptable or not.\n    :param targetTime: The time before which all jobs should at least be started.\n\n    :returns: The minimum number of minimal node allocations estimated to be required to run all\n              the jobs in jobShapes.\n    '

    def __init__(self, nodeShapes, targetTime=defaultTargetTime):
        self.nodeShapes = sorted(nodeShapes)
        self.targetTime = targetTime
        self.nodeReservations = {nodeShape:[] for nodeShape in nodeShapes}

    def binPack(self, jobShapes):
        """Pack a list of jobShapes into the fewest nodes reasonable. Can be run multiple times."""
        logger.debug('Running bin packing for node shapes %s and %s job(s).', self.nodeShapes, len(jobShapes))
        jobShapes.sort()
        jobShapes.reverse()
        if not len(jobShapes) == 0:
            if not jobShapes[0] >= jobShapes[(-1)]:
                raise AssertionError
        for jS in jobShapes:
            self.addJobShape(jS)

    def addJobShape(self, jobShape):
        """
        Function adds the job to the first node reservation in which it will fit (this is the
        bin-packing aspect).
        """
        chosenNodeShape = None
        for nodeShape in self.nodeShapes:
            if NodeReservation(nodeShape).fits(jobShape):
                chosenNodeShape = nodeShape
                break

        if chosenNodeShape is None:
            logger.warning("Couldn't fit job with requirements %r into any nodes in the nodeTypes list." % jobShape)
            return
        nodeReservations = self.nodeReservations[chosenNodeShape]
        for nodeReservation in nodeReservations:
            if nodeReservation.attemptToAddJob(jobShape, chosenNodeShape, self.targetTime):
                return

        reservation = NodeReservation(chosenNodeShape)
        currentTimeAllocated = chosenNodeShape.wallTime
        adjustEndingReservationForJob(reservation, jobShape, 0)
        self.nodeReservations[chosenNodeShape].append(reservation)
        while currentTimeAllocated < jobShape.wallTime:
            extendThisReservation = NodeReservation(reservation.shape)
            currentTimeAllocated += chosenNodeShape.wallTime
            reservation.nReservation = extendThisReservation
            reservation = extendThisReservation

    def getRequiredNodes(self):
        """
        Returns a dict from node shape to number of nodes required to run the packed jobs.
        """
        return {nodeShape:len(self.nodeReservations[nodeShape]) for nodeShape in self.nodeShapes}


class NodeReservation(object):
    __doc__ = '\n    Represents a node "reservation": the amount of resources that we\n    expect to be available on a given node at each point in time. To\n    represent the resources available in a reservation, we represent a\n    reservation as a linked list of NodeReservations, each giving the\n    resources free within a single timeslice.\n    '

    def __init__(self, shape):
        self.shape = shape
        self.nReservation = None

    def __str__(self):
        return '-------------------\nCurrent Reservation\n-------------------\nShape wallTime: %s\nShape memory: %s\nShape cores: %s\nShape disk: %s\nShape preempt: %s\n\nnReserv wallTime: %s\nnReserv memory: %s\nnReserv cores: %s\nnReserv disk: %s\nnReserv preempt: %s\n\nTime slices: %s\n\n' % (
         self.shape.wallTime,
         self.shape.memory,
         self.shape.cores,
         self.shape.disk,
         self.shape.preemptable,
         self.nReservation.shape.wallTime if self.nReservation is not None else str(None),
         self.nReservation.shape.memory if self.nReservation is not None else str(None),
         self.nReservation.shape.cores if self.nReservation is not None else str(None),
         self.nReservation.shape.disk if self.nReservation is not None else str(None),
         self.nReservation.shape.preemptable if self.nReservation is not None else str(None),
         str(len(self.shapes())))

    def fits(self, jobShape):
        """Check if a job shape's resource requirements will fit within this allocation."""
        return jobShape.memory <= self.shape.memory and jobShape.cores <= self.shape.cores and jobShape.disk <= self.shape.disk and (jobShape.preemptable or not self.shape.preemptable)

    def shapes(self):
        """Get all time-slice shapes, in order, from this reservation on."""
        shapes = []
        curRes = self
        while curRes is not None:
            shapes.append(curRes.shape)
            curRes = curRes.nReservation

        return shapes

    def subtract(self, jobShape):
        """
        Subtracts the resources necessary to run a jobShape from the reservation.
        """
        self.shape = Shape(self.shape.wallTime, self.shape.memory - jobShape.memory, self.shape.cores - jobShape.cores, self.shape.disk - jobShape.disk, self.shape.preemptable)

    def attemptToAddJob(self, jobShape, nodeShape, targetTime):
        """
        Attempt to pack a job into this reservation timeslice and/or the reservations after it.

        jobShape is the Shape of the job requirements, nodeShape is the Shape of the node this
        is a reservation for, and targetTime is the maximum time to wait before starting this job.
        """
        startingReservation = self
        endingReservation = startingReservation
        availableTime = 0
        startingReservationTime = 0
        while endingReservation.fits(jobShape):
            availableTime += endingReservation.shape.wallTime
            if availableTime >= jobShape.wallTime:
                timeSlice = 0
                while startingReservation != endingReservation:
                    startingReservation.subtract(jobShape)
                    timeSlice += startingReservation.shape.wallTime
                    startingReservation = startingReservation.nReservation

                assert jobShape.wallTime - timeSlice <= startingReservation.shape.wallTime
                adjustEndingReservationForJob(endingReservation, jobShape, timeSlice)
                return True
            if endingReservation.nReservation == None:
                if startingReservation == self:
                    endingReservation.nReservation = NodeReservation(nodeShape)
            else:
                if startingReservationTime + availableTime + endingReservation.shape.wallTime <= targetTime:
                    startingReservation = endingReservation.nReservation
                    startingReservationTime += availableTime + endingReservation.shape.wallTime
                    availableTime = 0
                else:
                    break
                endingReservation = endingReservation.nReservation
                if endingReservation is None:
                    break

        return False


def adjustEndingReservationForJob(reservation, jobShape, wallTime):
    """
    Add a job to an ending reservation that ends at wallTime, splitting
    the reservation if the job doesn't fill the entire timeslice.
    """
    if jobShape.wallTime - wallTime < reservation.shape.wallTime:
        reservation.shape, nS = split(reservation.shape, jobShape, jobShape.wallTime - wallTime)
        nS.nReservation = reservation.nReservation
        reservation.nReservation = nS
    else:
        reservation.subtract(jobShape)


def split(nodeShape, jobShape, wallTime):
    """
    Partition a node allocation into two to fit the job, returning the
    modified shape of the node and a new node reservation for
    the extra time that the job didn't fill.
    """
    return (
     Shape(wallTime, nodeShape.memory - jobShape.memory, nodeShape.cores - jobShape.cores, nodeShape.disk - jobShape.disk, nodeShape.preemptable),
     NodeReservation(Shape(nodeShape.wallTime - wallTime, nodeShape.memory, nodeShape.cores, nodeShape.disk, nodeShape.preemptable)))


def binPacking(nodeShapes, jobShapes, goalTime):
    bpf = BinPackedFit(nodeShapes, goalTime)
    bpf.binPack(jobShapes)
    return bpf.getRequiredNodes()


class ClusterScaler(object):

    def __init__(self, provisioner, leader, config):
        """
        Class manages automatically scaling the number of worker nodes.

        :param AbstractProvisioner provisioner: Provisioner instance to scale.
        :param toil.leader.Leader leader:
        :param Config config: Config object from which to draw parameters.
        """
        self.provisioner = provisioner
        self.leader = leader
        self.config = config
        self.static = {}
        self.jobNameToAvgRuntime = {}
        self.jobNameToNumCompleted = {}
        self.totalAvgRuntime = 0.0
        self.totalJobsCompleted = 0
        self.targetTime = config.targetTime
        if self.targetTime <= 0:
            raise RuntimeError('targetTime (%s) must be a positive integer!' % self.targetTime)
        else:
            self.betaInertia = config.betaInertia
            if not 0.0 <= self.betaInertia <= 0.9:
                raise RuntimeError('betaInertia (%f) must be between 0.0 and 0.9!' % self.betaInertia)
            self.nodeTypes = provisioner.nodeTypes
            self.nodeShapes = provisioner.nodeShapes
            self.nodeShapeToType = dict(zip(self.nodeShapes, self.nodeTypes))
            self.ignoredNodes = set()
            self.preemptableNodeDeficit = {nodeType:0 for nodeType in self.nodeTypes}
            self.previousWeightedEstimate = {nodeShape:0.0 for nodeShape in self.nodeShapes}
            assert len(self.nodeShapes) > 0
        minNodes = config.minNodes
        if minNodes is None:
            minNodes = [0 for node in self.nodeTypes]
        maxNodes = config.maxNodes
        while len(maxNodes) < len(self.nodeTypes):
            maxNodes.append(maxNodes[0])

        while len(minNodes) < len(self.nodeTypes):
            minNodes.append(0)

        self.minNodes = dict(zip(self.nodeShapes, minNodes))
        self.maxNodes = dict(zip(self.nodeShapes, maxNodes))
        self.nodeShapes.sort()
        totalNodes = defaultdict(int)
        if isinstance(leader.batchSystem, AbstractScalableBatchSystem):
            for preemptable in (True, False):
                nodes = []
                for nodeShape, nodeType in self.nodeShapeToType.items():
                    nodes_thisType = leader.provisioner.getProvisionedWorkers(nodeType=nodeType, preemptable=preemptable)
                    totalNodes[nodeShape] += len(nodes_thisType)
                    nodes.extend(nodes_thisType)

                self.setStaticNodes(nodes, preemptable)

        logger.debug('Starting with the following nodes in the cluster: %s' % totalNodes)
        if not sum(config.maxNodes) > 0:
            raise RuntimeError('Not configured to create nodes of any type.')

    def _round(self, number):
        """
        Helper function for rounding-as-taught-in-school (X.5 rounds to X+1 if positive).
        Python 3 now rounds 0.5 to whichever side is even (i.e. 2.5 rounds to 2).
        
        :param int number: a float to round.
        :return: closest integer to number, rounding ties away from 0.
        """
        sign = 1 if number >= 0 else -1
        rounded = int(round(number))
        nextRounded = int(round(number + 1 * sign))
        if nextRounded == rounded:
            return rounded
        if nextRounded == rounded + 1 * sign:
            return rounded
        if nextRounded == rounded + 2 * sign:
            return rounded + 1 * sign
        raise RuntimeError('Could not round {}'.format(number))

    def getAverageRuntime(self, jobName, service=False):
        if service:
            return self.targetTime * 24 + 3600
        else:
            if jobName in self.jobNameToAvgRuntime:
                return self.jobNameToAvgRuntime[jobName]
            if self.totalAvgRuntime > 0:
                return self.totalAvgRuntime
            return 1.0

    def addCompletedJob(self, job, wallTime):
        """
        Adds the shape of a completed job to the queue, allowing the scalar to use the last N
        completed jobs in factoring how many nodes are required in the cluster.
        :param toil.job.JobNode job: The memory, core and disk requirements of the completed job
        :param int wallTime: The wall-time taken to complete the job in seconds.
        """
        if job.jobName in self.jobNameToAvgRuntime:
            prevAvg = self.jobNameToAvgRuntime[job.jobName]
            prevNum = self.jobNameToNumCompleted[job.jobName]
            self.jobNameToAvgRuntime[job.jobName] = float(prevAvg * prevNum + wallTime) / (prevNum + 1)
            self.jobNameToNumCompleted[job.jobName] += 1
        else:
            self.jobNameToAvgRuntime[job.jobName] = wallTime
            self.jobNameToNumCompleted[job.jobName] = 1
        self.totalJobsCompleted += 1
        self.totalAvgRuntime = float(self.totalAvgRuntime * (self.totalJobsCompleted - 1) + wallTime) / self.totalJobsCompleted

    def setStaticNodes(self, nodes, preemptable):
        """
        Used to track statically provisioned nodes. This method must be called
        before any auto-scaled nodes are provisioned.

        These nodes are treated differently than auto-scaled nodes in that they should
        not be automatically terminated.

        :param nodes: list of Node objects
        """
        prefix = 'non-' if not preemptable else ''
        logger.debug('Adding %s to %spreemptable static nodes', nodes, prefix)
        if nodes is not None:
            self.static[preemptable] = {node.privateIP:node for node in nodes}

    def getStaticNodes(self, preemptable):
        """
        Returns nodes set in setStaticNodes().

        :param preemptable:
        :return: Statically provisioned nodes.
        """
        return self.static[preemptable]

    def smoothEstimate(self, nodeShape, estimatedNodeCount):
        """
        Smooth out fluctuations in the estimate for this node compared to
        previous runs. Returns an integer.
        """
        weightedEstimate = (1 - self.betaInertia) * estimatedNodeCount + self.betaInertia * self.previousWeightedEstimate[nodeShape]
        self.previousWeightedEstimate[nodeShape] = weightedEstimate
        return self._round(weightedEstimate)

    def getEstimatedNodeCounts(self, queuedJobShapes, currentNodeCounts):
        """
        Given the resource requirements of queued jobs and the current size of the cluster, returns
        a dict mapping from nodeShape to the number of nodes we want in the cluster right now.
        """
        nodesToRunQueuedJobs = binPacking(jobShapes=queuedJobShapes, nodeShapes=(self.nodeShapes),
          goalTime=(self.targetTime))
        estimatedNodeCounts = {}
        for nodeShape in self.nodeShapes:
            nodeType = self.nodeShapeToType[nodeShape]
            logger.debug('Nodes of type %s to run queued jobs = %s' % (
             nodeType, nodesToRunQueuedJobs[nodeShape]))
            estimatedNodeCount = 0 if nodesToRunQueuedJobs[nodeShape] == 0 else max(1, self._round(nodesToRunQueuedJobs[nodeShape]))
            logger.debug('Estimating %i nodes of shape %s' % (estimatedNodeCount, nodeShape))
            estimatedNodeCount = self.smoothEstimate(nodeShape, estimatedNodeCount)
            if not nodeShape.preemptable:
                compensation = self.config.preemptableCompensation
                assert 0.0 <= compensation <= 1.0
                compensationNodes = self._round(self.preemptableNodeDeficit[nodeType] * compensation)
                if compensationNodes > 0:
                    logger.debug('Adding %d non-preemptable nodes of type %s to compensate for a deficit of %d preemptable ones.', compensationNodes, nodeType, self.preemptableNodeDeficit[nodeType])
                estimatedNodeCount += compensationNodes
            logger.debug('Currently %i nodes of type %s in cluster' % (currentNodeCounts[nodeShape],
             nodeType))
            if self.leader.toilMetrics:
                self.leader.toilMetrics.logClusterSize(nodeType=nodeType, currentSize=(currentNodeCounts[nodeShape]),
                  desiredSize=estimatedNodeCount)
            if estimatedNodeCount > self.maxNodes[nodeShape]:
                logger.debug('Limiting the estimated number of necessary %s (%s) to the configured maximum (%s).', nodeType, estimatedNodeCount, self.maxNodes[nodeShape])
                estimatedNodeCount = self.maxNodes[nodeShape]
            else:
                if estimatedNodeCount < self.minNodes[nodeShape]:
                    logger.debug('Raising the estimated number of necessary %s (%s) to the configured minimum (%s).', nodeType, estimatedNodeCount, self.minNodes[nodeShape])
                    estimatedNodeCount = self.minNodes[nodeShape]
            estimatedNodeCounts[nodeShape] = estimatedNodeCount

        return estimatedNodeCounts

    def updateClusterSize(self, estimatedNodeCounts):
        """
        Given the desired and current size of the cluster, attempts to launch/remove instances to
        get to the desired size. Also attempts to remove ignored nodes that were marked for graceful
        removal.

        Returns the new size of the cluster.
        """
        newNodeCounts = defaultdict(int)
        for nodeShape, estimatedNodeCount in estimatedNodeCounts.items():
            nodeType = self.nodeShapeToType[nodeShape]
            newNodeCount = self.setNodeCount(nodeType=nodeType, numNodes=estimatedNodeCount, preemptable=(nodeShape.preemptable))
            if nodeShape.preemptable:
                if newNodeCount < estimatedNodeCount:
                    deficit = estimatedNodeCount - newNodeCount
                    logger.debug('Preemptable scaler detected deficit of %d nodes of type %s.' % (deficit, nodeType))
                    self.preemptableNodeDeficit[nodeType] = deficit
                else:
                    self.preemptableNodeDeficit[nodeType] = 0
            newNodeCounts[nodeShape] = newNodeCount

        self._terminateIgnoredNodes()
        return newNodeCounts

    def setNodeCount(self, nodeType, numNodes, preemptable=False, force=False):
        """
        Attempt to grow or shrink the number of preemptable or non-preemptable worker nodes in
        the cluster to the given value, or as close a value as possible, and, after performing
        the necessary additions or removals of worker nodes, return the resulting number of
        preemptable or non-preemptable nodes currently in the cluster.

        :param str nodeType: The node type to add or remove.

        :param int numNodes: Desired size of the cluster

        :param bool preemptable: whether the added nodes will be preemptable, i.e. whether they
               may be removed spontaneously by the underlying platform at any time.

        :param bool force: If False, the provisioner is allowed to deviate from the given number
               of nodes. For example, when downsizing a cluster, a provisioner might leave nodes
               running if they have active jobs running on them.

        :rtype: int :return: the number of worker nodes in the cluster after making the necessary
                adjustments. This value should be, but is not guaranteed to be, close or equal to
                the `numNodes` argument. It represents the closest possible approximation of the
                actual cluster size at the time this method returns.
        """
        for attempt in retry(predicate=(self.provisioner.retryPredicate)):
            with attempt:
                workerInstances = self.getNodes(preemptable=preemptable)
                logger.debug('Cluster contains %i instances' % len(workerInstances))
                workerInstances = {node:workerInstances[node] for node in workerInstances if node.nodeType == nodeType}
                ignoredNodes = [node for node in workerInstances if node.privateIP in self.ignoredNodes]
                numIgnoredNodes = len(ignoredNodes)
                numCurrentNodes = len(workerInstances)
                logger.debug('Cluster contains %i instances of type %s (%i ignored and draining jobs until they can be safely terminated)' % (
                 numCurrentNodes, nodeType, numIgnoredNodes))
                if not force:
                    delta = numNodes - (numCurrentNodes - numIgnoredNodes)
                else:
                    delta = numNodes - numCurrentNodes
                if delta > 0 and numIgnoredNodes > 0:
                    numNodesToUnignore = min(delta, numIgnoredNodes)
                    logger.debug('Unignoring %i nodes because we want to scale back up again.' % numNodesToUnignore)
                    delta -= numNodesToUnignore
                    for node in ignoredNodes[:numNodesToUnignore]:
                        self.ignoredNodes.remove(node.privateIP)
                        self.leader.batchSystem.unignoreNode(node.privateIP)

                if delta > 0:
                    logger.info('Adding %i %s nodes to get to desired cluster size of %i.', delta, 'preemptable' if preemptable else 'non-preemptable', numNodes)
                    numNodes = numCurrentNodes + self._addNodes(nodeType, numNodes=delta, preemptable=preemptable)
                else:
                    if delta < 0:
                        logger.info('Removing %i %s nodes to get to desired cluster size of %i.', -delta, 'preemptable' if preemptable else 'non-preemptable', numNodes)
                        numNodes = numCurrentNodes - self._removeNodes(workerInstances, nodeType=nodeType,
                          numNodes=(-delta),
                          preemptable=preemptable,
                          force=force)
                    else:
                        if not force:
                            logger.debug('Cluster (minus ignored nodes) already at desired size of %i. Nothing to do.', numNodes)
                        else:
                            logger.debug('Cluster already at desired size of %i. Nothing to do.', numNodes)

        return numNodes

    def _addNodes(self, nodeType, numNodes, preemptable):
        return self.provisioner.addNodes(nodeType=nodeType, numNodes=numNodes, preemptable=preemptable)

    def _removeNodes(self, nodeToNodeInfo, nodeType, numNodes, preemptable=False, force=False):
        if isinstance(self.leader.batchSystem, AbstractScalableBatchSystem):
            nodeToNodeInfo = self.getNodes(preemptable)
            nodeToNodeInfo = {node:nodeToNodeInfo[node] for node in nodeToNodeInfo if node.nodeType == nodeType}
            nodesToTerminate = self.chooseNodes(nodeToNodeInfo, force, preemptable=preemptable)
            nodesToTerminate = nodesToTerminate[:numNodes]
            logger.debug('Nodes considered to terminate: %s', ' '.join(map(str, nodeToNodeInfo)))
            for node, nodeInfo in nodesToTerminate:
                self.ignoredNodes.add(node.privateIP)
                self.leader.batchSystem.ignoreNode(node.privateIP)

            if not force:
                nodesToTerminate = [(node, nodeInfo) for node, nodeInfo in nodesToTerminate if nodeInfo is not None if nodeInfo.workers < 1]
            nodesToTerminate = {node:nodeInfo for node, nodeInfo in nodesToTerminate}
            nodeToNodeInfo = nodesToTerminate
        else:
            nodeToNodeInfo = sorted(nodeToNodeInfo, key=(lambda x: x.remainingBillingInterval()))
            nodeToNodeInfo = [instance for instance in islice(nodeToNodeInfo, numNodes)]
        logger.debug('Terminating %i instance(s).', len(nodeToNodeInfo))
        if nodeToNodeInfo:
            for node in nodeToNodeInfo:
                if node.privateIP in self.ignoredNodes:
                    self.ignoredNodes.remove(node.privateIP)
                    self.leader.batchSystem.unignoreNode(node.privateIP)

            self.provisioner.terminateNodes(nodeToNodeInfo)
        return len(nodeToNodeInfo)

    def _terminateIgnoredNodes(self):
        nodeToNodeInfo = self.getNodes(preemptable=None)
        allNodeIPs = [node.privateIP for node in nodeToNodeInfo]
        terminatedIPs = set([ip for ip in self.ignoredNodes if ip not in allNodeIPs])
        for ip in terminatedIPs:
            self.ignoredNodes.remove(ip)
            self.leader.batchSystem.unignoreNode(ip)

        logger.debug('There are %i nodes being ignored by the batch system, checking if they can be terminated' % len(self.ignoredNodes))
        nodeToNodeInfo = {node:nodeToNodeInfo[node] for node in nodeToNodeInfo if node.privateIP in self.ignoredNodes}
        nodeToNodeInfo = {node:nodeToNodeInfo[node] for node in nodeToNodeInfo if nodeToNodeInfo[node].workers < 1}
        for node in nodeToNodeInfo:
            self.ignoredNodes.remove(node.privateIP)
            self.leader.batchSystem.unignoreNode(node.privateIP)

        if len(nodeToNodeInfo) > 0:
            logger.debug('Terminating %i nodes that were being ignored by the batch system.' % len(nodeToNodeInfo))
            self.provisioner.terminateNodes(nodeToNodeInfo)

    def chooseNodes(self, nodeToNodeInfo, force=False, preemptable=False):
        nodesToTerminate = []
        for node, nodeInfo in list(nodeToNodeInfo.items()):
            if node is None:
                logger.debug('Node with info %s was not found in our node list', nodeInfo)
            else:
                staticNodes = self.getStaticNodes(preemptable)
                prefix = 'non-' if not preemptable else ''
                if node.privateIP in staticNodes:
                    logger.debug('Found %s in %spreemptable static nodes', node.privateIP, prefix)
                    continue
                else:
                    logger.debug('Did not find %s in %spreemptable static nodes', node.privateIP, prefix)
                nodesToTerminate.append((node, nodeInfo))

        nodesToTerminate.sort(key=(lambda node_nodeInfo: (
         node_nodeInfo[1].workers if node_nodeInfo[1] else 1, node_nodeInfo[0].remainingBillingInterval())))
        return nodesToTerminate

    def getNodes(self, preemptable):
        """
        Returns a dictionary mapping node identifiers of preemptable or non-preemptable nodes to
        NodeInfo objects, one for each node.

        This method is the definitive source on nodes in cluster, & is responsible for consolidating
        cluster state between the provisioner & batch system.

        :param bool preemptable: If True (False) only (non-)preemptable nodes will be returned.
               If None, all nodes will be returned.

        :rtype: dict[Node, NodeInfo]
        """

        def _getInfo(allMesosNodes, ip):
            info = None
            try:
                info = allMesosNodes[ip]
            except KeyError:
                info = NodeInfo(coresTotal=1, coresUsed=0, requestedCores=0, memoryTotal=1,
                  memoryUsed=0,
                  requestedMemory=0,
                  workers=0)
            else:
                inUse = self.leader.batchSystem.nodeInUse(ip)
                if not inUse:
                    if info:
                        info.workers = 0
                return info

        allMesosNodes = self.leader.batchSystem.getNodes(preemptable, timeout=None)
        recentMesosNodes = self.leader.batchSystem.getNodes(preemptable)
        provisionerNodes = self.provisioner.getProvisionedWorkers(nodeType=None, preemptable=preemptable)
        if len(recentMesosNodes) != len(provisionerNodes):
            logger.debug('Consolidating state between mesos and provisioner')
        nodeToInfo = {}
        for node, ip in ((node, node.privateIP) for node in provisionerNodes):
            info = None
            if ip not in recentMesosNodes:
                logger.debug('Worker node at %s is not reporting executor information', ip)
                info = _getInfo(allMesosNodes, ip)
            else:
                info = recentMesosNodes[ip]
            nodeToInfo[node] = info

        return nodeToInfo

    def shutDown(self):
        logger.debug('Forcing provisioner to reduce cluster size to zero.')
        for nodeShape in self.nodeShapes:
            preemptable = nodeShape.preemptable
            nodeType = self.nodeShapeToType[nodeShape]
            self.setNodeCount(nodeType=nodeType, numNodes=0, preemptable=preemptable, force=True)


class ScalerThread(ExceptionalThread):
    __doc__ = '\n    A thread that automatically scales the number of either preemptable or non-preemptable worker\n    nodes according to the resource requirements of the queued jobs.\n    The scaling calculation is essentially as follows: start with 0 estimated worker nodes. For\n    each queued job, check if we expect it can be scheduled into a worker node before a certain time\n    (currently one hour). Otherwise, attempt to add a single new node of the smallest type that\n    can fit that job.\n    At each scaling decision point a comparison between the current, C, and newly estimated\n    number of nodes is made. If the absolute difference is less than beta * C then no change\n    is made, else the size of the cluster is adapted. The beta factor is an inertia parameter\n    that prevents continual fluctuations in the number of nodes.\n    '

    def __init__(self, provisioner, leader, config):
        super(ScalerThread, self).__init__(name='scaler')
        self.scaler = ClusterScaler(provisioner, leader, config)
        self.stop = False
        self.stats = None
        if config.clusterStats:
            logger.debug('Starting up cluster statistics...')
            self.stats = ClusterStats(leader.config.clusterStats, leader.batchSystem, provisioner.clusterName)
            for preemptable in (True, False):
                self.stats.startStats(preemptable=preemptable)

            logger.debug('...Cluster stats started.')

    def check(self):
        """
        Attempt to join any existing scaler threads that may have died or finished. This insures
        any exceptions raised in the threads are propagated in a timely fashion.
        """
        try:
            self.join(timeout=0)
        except Exception as e:
            logger.exception(e)
            raise

    def shutdown(self):
        """
        Shutdown the cluster.
        """
        self.stop = True
        if self.stats:
            self.stats.shutDownStats()
        self.join()

    def addCompletedJob(self, job, wallTime):
        self.scaler.addCompletedJob(job, wallTime)

    def tryRun(self):
        while not self.stop:
            with throttle(self.scaler.config.scaleInterval):
                try:
                    queuedJobs = self.scaler.leader.getJobs()
                    queuedJobShapes = [Shape(wallTime=self.scaler.getAverageRuntime(jobName=(job.jobName), service=(isinstance(job, ServiceJobNode))), memory=(job.memory), cores=(job.cores), disk=(job.disk), preemptable=(job.preemptable)) for job in queuedJobs]
                    currentNodeCounts = {}
                    for nodeShape in self.scaler.nodeShapes:
                        nodeType = self.scaler.nodeShapeToType[nodeShape]
                        currentNodeCounts[nodeShape] = len(self.scaler.leader.provisioner.getProvisionedWorkers(nodeType=nodeType, preemptable=(nodeShape.preemptable)))

                    estimatedNodeCounts = self.scaler.getEstimatedNodeCounts(queuedJobShapes, currentNodeCounts)
                    self.scaler.updateClusterSize(estimatedNodeCounts)
                    if self.stats:
                        self.stats.checkStats()
                except:
                    logger.exception('Exception encountered in scaler thread. Making a best-effort attempt to keep going, but things may go wrong from now on.')

        self.scaler.shutDown()


class ClusterStats(object):

    def __init__(self, path, batchSystem, clusterName):
        logger.debug('Initializing cluster statistics')
        self.stats = {}
        self.statsThreads = []
        self.statsPath = path
        self.stop = False
        self.clusterName = clusterName
        self.batchSystem = batchSystem
        self.scaleable = isinstance(self.batchSystem, AbstractScalableBatchSystem) if batchSystem else False

    def shutDownStats(self):
        if self.stop:
            return

        def getFileName():
            extension = '.json'
            file = '%s-stats' % self.clusterName
            counter = 0
            while True:
                suffix = str(counter).zfill(3) + extension
                fullName = os.path.join(self.statsPath, file + suffix)
                if not os.path.exists(fullName):
                    return fullName
                counter += 1

        if self.statsPath:
            if self.scaleable:
                self.stop = True
                for thread in self.statsThreads:
                    thread.join()

                fileName = getFileName()
                with open(fileName, 'w') as (f):
                    json.dump(self.stats, f)

    def startStats(self, preemptable):
        thread = ExceptionalThread(target=(self._gatherStats), args=[preemptable])
        thread.start()
        self.statsThreads.append(thread)

    def checkStats(self):
        for thread in self.statsThreads:
            thread.join(timeout=0)

    def _gatherStats(self, preemptable):

        def toDict(nodeInfo):
            return dict(memory=(nodeInfo.memoryUsed), cores=(nodeInfo.coresUsed),
              memoryTotal=(nodeInfo.memoryTotal),
              coresTotal=(nodeInfo.coresTotal),
              requestedCores=(nodeInfo.requestedCores),
              requestedMemory=(nodeInfo.requestedMemory),
              workers=(nodeInfo.workers),
              time=(time.time()))

        if self.scaleable:
            logger.debug('Starting to gather statistics')
            stats = {}
            try:
                while not self.stop:
                    nodeInfo = self.batchSystem.getNodes(preemptable)
                    for nodeIP in list(nodeInfo.keys()):
                        nodeStats = nodeInfo[nodeIP]
                        if nodeStats is not None:
                            nodeStats = toDict(nodeStats)
                            try:
                                stats[nodeIP].append(nodeStats)
                            except KeyError:
                                stats[nodeIP] = [
                                 nodeStats]

                    time.sleep(60)

            finally:
                threadName = 'Preemptable' if preemptable else 'Non-preemptable'
                logger.debug('%s provisioner stats thread shut down successfully.', threadName)
                self.stats[threadName] = stats