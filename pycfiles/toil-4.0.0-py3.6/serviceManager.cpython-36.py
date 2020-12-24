# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/serviceManager.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 10924 bytes
from __future__ import absolute_import
from builtins import map
from builtins import object
import logging, time
from threading import Thread, Event
from toil.lib.throttle import throttle
from six.moves.queue import Empty, Queue
logger = logging.getLogger(__name__)

class ServiceManager(object):
    __doc__ = '\n    Manages the scheduling of services.\n    '

    def __init__(self, jobStore, toilState):
        logger.debug('Initializing service manager')
        self.jobStore = jobStore
        self.toilState = toilState
        self.jobGraphsWithServicesBeingStarted = set()
        self._terminate = Event()
        self._jobGraphsWithServicesToStart = Queue()
        self._jobGraphsWithServicesThatHaveStarted = Queue()
        self._serviceJobGraphsToStart = Queue()
        self.jobsIssuedToServiceManager = 0
        self._serviceStarter = Thread(target=(self._startServices), args=(
         self._jobGraphsWithServicesToStart,
         self._jobGraphsWithServicesThatHaveStarted,
         self._serviceJobGraphsToStart, self._terminate,
         self.jobStore),
          daemon=True)

    def start(self):
        """
        Start the service scheduling thread.
        """
        self._serviceStarter.start()

    def scheduleServices(self, jobGraph):
        """
        Schedule the services of a job asynchronously.
        When the job's services are running the jobGraph for the job will
        be returned by toil.leader.ServiceManager.getJobGraphsWhoseServicesAreRunning.

        :param toil.jobGraph.JobGraph jobGraph: wrapper of job with services to schedule.
        """
        self.jobGraphsWithServicesBeingStarted.add(jobGraph)
        self.jobsIssuedToServiceManager += sum(map(len, jobGraph.services)) + 1
        self._jobGraphsWithServicesToStart.put(jobGraph)

    def getJobGraphWhoseServicesAreRunning(self, maxWait):
        """
        :param float maxWait: Time in seconds to wait to get a jobGraph before returning
        :return: a jobGraph added to scheduleServices whose services are running, or None if
        no such job is available.
        :rtype: JobGraph
        """
        try:
            jobGraph = self._jobGraphsWithServicesThatHaveStarted.get(timeout=maxWait)
            self.jobGraphsWithServicesBeingStarted.remove(jobGraph)
            assert self.jobsIssuedToServiceManager >= 0
            self.jobsIssuedToServiceManager -= 1
            return jobGraph
        except Empty:
            return

    def getServiceJobsToStart(self, maxWait):
        """
        :param float maxWait: Time in seconds to wait to get a job before returning.
        :return: a tuple of (serviceJobStoreID, memory, cores, disk, ..) representing
        a service job to start.
        :rtype: toil.job.ServiceJobNode
        """
        try:
            serviceJob = self._serviceJobGraphsToStart.get(timeout=maxWait)
            assert self.jobsIssuedToServiceManager >= 0
            self.jobsIssuedToServiceManager -= 1
            return serviceJob
        except Empty:
            return

    def killServices(self, services, error=False):
        """
        :param dict services: Maps service jobStoreIDs to the communication flags for the service
        """
        for serviceJobStoreID in services:
            serviceJob = services[serviceJobStoreID]
            if error:
                self.jobStore.deleteFile(serviceJob.errorJobStoreID)
            self.jobStore.deleteFile(serviceJob.terminateJobStoreID)

    def isActive(self, serviceJobNode):
        """
        Returns true if the service job has not been told to terminate.
        :rtype: boolean
        """
        return self.jobStore.fileExists(serviceJobNode.terminateJobStoreID)

    def isRunning(self, serviceJobNode):
        """
        Returns true if the service job has started and is active
        :rtype: boolean
        """
        return not self.jobStore.fileExists(serviceJobNode.startJobStoreID) and self.isActive(serviceJobNode)

    def check(self):
        """
        Check on the service manager thread.
        :raise RuntimeError: If the underlying thread has quit.
        """
        if not self._serviceStarter.is_alive():
            raise RuntimeError('Service manager has quit')

    def shutdown(self):
        """
        Cleanly terminate worker threads starting and killing services. Will block
        until all services are started and blocked.
        """
        logger.debug('Waiting for service manager thread to finish ...')
        startTime = time.time()
        self._terminate.set()
        self._serviceStarter.join()
        for services in list(self.toilState.servicesIssued.values()):
            self.killServices(services, error=True)

        logger.debug('... finished shutting down the service manager. Took %s seconds', time.time() - startTime)

    @staticmethod
    def _startServices(jobGraphsWithServicesToStart, jobGraphsWithServicesThatHaveStarted, serviceJobsToStart, terminate, jobStore):
        """
        Thread used to schedule services.
        """
        servicesThatAreStarting = set()
        servicesRemainingToStartForJob = {}
        serviceToJobGraph = {}
        while True:
            with throttle(1.0):
                if terminate.is_set():
                    logger.debug('Received signal to quit starting services.')
                    break
                try:
                    jobGraph = jobGraphsWithServicesToStart.get_nowait()
                    if len(jobGraph.services) > 1:
                        blockUntilServiceGroupIsStarted(jobGraph, jobGraphsWithServicesThatHaveStarted, serviceJobsToStart, terminate, jobStore)
                        continue
                    for serviceJob in jobGraph.services[0]:
                        serviceToJobGraph[serviceJob] = jobGraph

                    servicesRemainingToStartForJob[jobGraph] = len(jobGraph.services[0])
                    for serviceJob in jobGraph.services[0]:
                        logger.debug('Service manager is starting service job: %s, start ID: %s', serviceJob, serviceJob.startJobStoreID)
                        serviceJobsToStart.put(serviceJob)

                    servicesThatAreStarting.update(jobGraph.services[0])
                except Empty:
                    pass

                for serviceJob in list(servicesThatAreStarting):
                    if not jobStore.fileExists(serviceJob.startJobStoreID):
                        servicesThatAreStarting.remove(serviceJob)
                        parentJob = serviceToJobGraph[serviceJob]
                        servicesRemainingToStartForJob[parentJob] -= 1
                        assert servicesRemainingToStartForJob[parentJob] >= 0
                        del serviceToJobGraph[serviceJob]

                jobGraphsToRemove = set()
                for jobGraph, remainingServices in servicesRemainingToStartForJob.items():
                    if remainingServices == 0:
                        jobGraphsWithServicesThatHaveStarted.put(jobGraph)
                        jobGraphsToRemove.add(jobGraph)

                for jobGraph in jobGraphsToRemove:
                    del servicesRemainingToStartForJob[jobGraph]


def blockUntilServiceGroupIsStarted(jobGraph, jobGraphsWithServicesThatHaveStarted, serviceJobsToStart, terminate, jobStore):
    for serviceJobList in jobGraph.services:
        for serviceJob in serviceJobList:
            logger.debug('Service manager is starting service job: %s, start ID: %s', serviceJob, serviceJob.startJobStoreID)
            assert jobStore.fileExists(serviceJob.startJobStoreID)
            serviceJobsToStart.put(serviceJob)

        for serviceJob in serviceJobList:
            while jobStore.fileExists(serviceJob.startJobStoreID):
                time.sleep(1.0)
                if terminate.is_set():
                    return

    jobGraphsWithServicesThatHaveStarted.put(jobGraph)