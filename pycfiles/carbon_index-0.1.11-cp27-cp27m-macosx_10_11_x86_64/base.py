# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/gabrielfalcao/projects/personal/carbontube/carbontube/storage/base.py
# Compiled at: 2017-06-08 00:31:56


class BaseStorageBackend(object):
    """base class for storage backends"""

    def __init__(self, name, *args, **kw):
        self.pipeline_name = name
        self.initialize(*args, **kw)

    def initialize(self):
        """backend-specific constructor. This method must be overriden by subclasses
        in order to setup database connections and such"""
        pass

    def connect(self):
        """this method is called by the pipeline once it started to listen on
        zmq sockets, so this is also an appropriate time to implement
        your own connection to a database in a backend subclass pass
        """
        pass

    def register_worker(self, worker):
        """register the worker as available. must return a boolean. True if
        the worker was successfully registered, False otherwise"""
        return True

    def unregister_worker(self, worker):
        """unregisters the worker completely, removing it from the roster"""
        pass

    def enqueue_job(self, job):
        """adds the job to its appropriate queue name"""
        pass

    def consume_job_of_type(self, job_type):
        """dequeues a job for the given type. must return None when no job is
        ready.

        Make sure to requeue this job in case it could not be fed into
        an immediate worker.
        """
        pass

    def get_next_available_worker_for_type(self, job_type):
        """randomly picks a workers that is currently available"""
        pass