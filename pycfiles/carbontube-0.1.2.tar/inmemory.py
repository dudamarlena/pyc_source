# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabrielfalcao/projects/personal/carbontube/carbontube/storage/inmemory.py
# Compiled at: 2017-06-08 00:31:56
import random
from collections import defaultdict
from carbontube.storage.base import BaseStorageBackend

class EphemeralStorageBackend(BaseStorageBackend):
    """in-memory storage backend. It dies with the process and has no
    option for persistence whatsoever. Used only for testing purposes."""

    def initialize(self):
        self.workers = {}
        self.workers_by_job_type = defaultdict(set)
        self.jobs_by_type = defaultdict(list)

    def connect(self):
        pass

    def register_worker(self, worker):
        if worker.id in self.workers:
            return False
        self.workers[worker.id] = worker
        self.workers_by_job_type[worker.job_type].add(worker.id)
        return True

    def unregister_worker(self, worker):
        self.workers.pop(worker.id, None)
        self.workers_by_job_type[worker.job_type].remove(worker.id)
        return

    def enqueue_job(self, job):
        self.jobs_by_type[job.type].append(job)

    def consume_job_of_type(self, job_type):
        try:
            return self.jobs_by_type[job_type].pop(0)
        except IndexError:
            return

        return

    def get_next_available_worker_for_type(self, job_type):
        worker_ids = list(self.workers_by_job_type[job_type])
        if not worker_ids:
            return
        else:
            try:
                wid = random.choice(worker_ids)
                return self.workers.get(wid)
            except KeyError:
                return

            return