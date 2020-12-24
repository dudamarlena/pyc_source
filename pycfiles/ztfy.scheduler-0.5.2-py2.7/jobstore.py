# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/jobstore.py
# Compiled at: 2012-10-22 06:18:07
__docformat__ = 'restructuredtext'
from apscheduler.jobstores.base import JobStore
from ztfy.utils.interfaces import IZEOConnection
from zope.component import getUtility, queryUtility
from zope.traversing.api import getParent, getPath

class ZODBJobsStore(JobStore):
    """ZODB jobs store"""

    def __new__(cls, scheduler_util, scheduler_process):
        zeo_connection_util = queryUtility(IZEOConnection, scheduler_util.zeo_connection)
        if zeo_connection_util is None:
            return
        else:
            return JobStore.__new__(cls, scheduler_util, scheduler_process)

    def __init__(self, scheduler_util, scheduler_process):
        self.scheduler_util = scheduler_util
        self.scheduler_path = getPath(scheduler_util)
        self.scheduler_process = scheduler_process

    def load_jobs(self):
        jobs = []
        for task in self.scheduler_util.tasks:
            trigger = task.getTrigger()
            if trigger is not None:
                zeo_connection = getUtility(IZEOConnection, name=getParent(task).zeo_connection, context=task)
                job = self.scheduler_process.add_job(trigger, task, args=None, kwargs={'zeo_settings': zeo_connection.getSettings()})
                job.id = task.internal_id
                jobs.append(job)

        self.jobs = jobs
        return

    def add_job(self, job):
        if job not in self.jobs:
            self.jobs.append(job)

    def update_job(self, job):
        for index, my_job in enumerate(self.jobs):
            if my_job.id == job.id:
                self.jobs[index] = job

    def remove_job(self, job):
        if job in self.jobs:
            self.jobs.remove(job)

    def close(self):
        pass

    def __repr__(self):
        return '<%s (ZODB=%s)>' % (self.__class__.__name__, self.scheduler_util.zeo_connection)