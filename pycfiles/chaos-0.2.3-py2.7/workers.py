# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/multiprocessing/workers.py
# Compiled at: 2015-07-28 07:52:50
""" Helper functions for working with python multiprocessing. """
from __future__ import absolute_import
import multiprocessing, logging, os

class Workers(object):
    """
        Container to register and handle multiple Worker processes.
        """
    worker_list = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def registerWorker(self, name, worker):
        """
                Register a new Worker, under the given descriptive name.

                Trying to register multiple workers under the same name will raise an Exception.

                Parameters
                ----------
                name: string
                        Name to register the given worker under.
                worker: multiprocessing.Process, or a subclass
                        Process object to register.
                """
        if not isinstance(worker, multiprocessing.Process):
            self.logger.error(('Process {0} is not actually a Process!').format(name))
            raise Exception(('Process {0} is not actually a Process!').format(name))
        if name in self.worker_list:
            self.logger.error(('Process {0} already registered!').format(name))
            raise Exception(('Process {0} already registered!').format(name))
        self.worker_list[name] = worker
        self.logger.debug(('Registered worker {0}').format(name))
        return worker

    def getWorkers(self):
        """
                Retrieve a list of names of all registered Workers.
                """
        return self.worker_list.keys()

    def getWorker(self, name):
        """
                Retrieve the Worker registered under the given name.

                If the given name does not exists in the Worker list, an Exception is raised.

                Parameters
                ----------
                name: string
                        Name of the Worker to retrieve
                """
        if name not in self.worker_list:
            self.logger.error(('Worker {0} is not registered!').format(name))
            raise Exception(('Worker {0} is not registered!').format(name))
        return self.worker_list[name]

    def unregisterWorker(self, name):
        """
                Unregister the Worker registered under the given name.

                Make sure that the given Worker is properly stopped, or that a reference is
                kept in another place. Once unregistered, this class will not keep any
                other references to the Worker.

                Parameters
                ----------
                name: string
                        Name of the Worker to unregister
                """
        if name not in self.worker_list:
            self.logger.error(('Worker {0} is not registered!').format(name))
            raise Exception(('Worker {0} is not registered!').format(name))
        del self.worker_list[name]
        self.logger.debug(('Unregistered worker {0}').format(name))

    def startAll(self):
        """
                Start all registered Workers.
                """
        self.logger.info('Starting all workers...')
        for worker in self.getWorkers():
            process = self.getWorker(worker)
            self.logger.debug(('Starting {0}').format(process.name))
            process.start()

        self.logger.info('Started all workers')

    def stopAll(self, timeout=10, stop=False):
        """
                Stop all registered Workers. This is method assumes that the Worker has already
                received a stop message somehow, and simply joins the Process until it dies, as 
                follows:

                1. The Worker is retrieved.
                2. The Worker is joined, and will wait until the Worker exits.
                3. The Worker is unregistered.
                4. If $stop = True, the main process is killed.
                """
        self.logger.info('Stopping all workers...')
        for worker in self.getWorkers():
            process = self.getWorker(worker)
            self.logger.debug(('Stopping {0}').format(process.name))
            if process.is_alive():
                process.join(timeout)
                if process.is_alive():
                    self.logger.warning(('Failed to stop {0}, terminating').format(process.name))
                    process.terminate()
            self.unregisterWorker(worker)

        self.logger.info('Stopped all workers')
        if stop:
            self.logger.fatal('Comitting suicide')
            os._exit(0)