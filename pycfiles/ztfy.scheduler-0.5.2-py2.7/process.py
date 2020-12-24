# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/process.py
# Compiled at: 2013-02-11 04:57:59
__docformat__ = 'restructuredtext'
from apscheduler.scheduler import Scheduler as SchedulerBase
from datetime import datetime
from threading import Thread
from transaction.interfaces import ITransactionManager
from ztfy.utils.interfaces import IZEOConnection
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility
from zope.traversing.api import getParent, getPath, traverse
from ztfy.scheduler.jobstore import ZODBJobsStore
from ztfy.scheduler.task import ImmediateTaskTrigger
from ztfy.utils.zodb import ZEOConnectionInfo
from ztfy.zmq.handler import ZMQMessageHandler
from ztfy.zmq.process import ZMQProcess

class TaskResettingThread(Thread):
    """Thread used to reset task scheduling
    
    Task reset is made in another thread, so that:
    - other transactions applied on updated tasks are visible
    - ZMQ request returns immediately to calling process
    """

    def __init__(self, process, settings):
        Thread.__init__(self)
        self.process = process
        self.settings = settings

    def _getConnection(self, settings):
        zeo_settings = settings.get('zeo')
        connection = ZEOConnectionInfo()
        connection.update(zeo_settings)
        return connection

    def run(self):
        settings = self.settings
        job_id = settings.get('job_id')
        if job_id is None:
            return
        else:
            with self._getConnection(settings) as (root):
                manager = None
                try:
                    root_folder = root.get(ZopePublication.root_name, None)
                    scheduler = self.process.scheduler
                    scheduler_util = traverse(root_folder, self.process.scheduler_path)
                    manager = ITransactionManager(scheduler_util)
                    manager.abort()
                    jobs_store = self.process.jobs_store
                    for job in jobs_store.jobs:
                        if job.id == job_id:
                            scheduler.unschedule_job(job)
                            break

                    task = scheduler_util.get(settings.get('task_name'))
                    if task is not None:
                        trigger = task.getTrigger()
                        if trigger is not None:
                            zeo_connection = getUtility(IZEOConnection, name=getParent(task).zeo_connection, context=task)
                            new_job = scheduler.add_job(trigger, task, args=None, kwargs={'zeo_settings': zeo_connection.getSettings()})
                            new_job.id = task.internal_id
                            jobs_store.update_job(new_job)
                finally:
                    if manager is not None:
                        manager.abort()

            return


class TaskRunnerThread(Thread):
    """Task immediate runner thread"""

    def __init__(self, process, settings):
        Thread.__init__(self)
        self.process = process
        self.settings = settings

    def _getConnection(self, settings):
        zeo_settings = settings.get('zeo')
        connection = ZEOConnectionInfo()
        connection.update(zeo_settings)
        return connection

    def run(self):
        settings = self.settings
        job_id = settings.get('job_id')
        if job_id is None:
            return
        else:
            with self._getConnection(settings) as (root):
                manager = None
                try:
                    root_folder = root.get(ZopePublication.root_name, None)
                    scheduler = self.process.scheduler
                    scheduler_util = traverse(root_folder, self.process.scheduler_path)
                    manager = ITransactionManager(scheduler_util)
                    manager.abort()
                    task = scheduler_util.get(settings.get('task_name'))
                    if task is not None:
                        trigger = ImmediateTaskTrigger()
                        zeo_connection = getUtility(IZEOConnection, name=getParent(task).zeo_connection, context=task)
                        new_job = scheduler.add_job(trigger, task, args=None, kwargs={'zeo_settings': zeo_connection.getSettings(), 'run_immediate': True})
                        new_job.id = '%s::%s' % (task.internal_id,
                         datetime.utcnow().strftime('%Y%m%d%H%M%S'))
                finally:
                    if manager is not None:
                        manager.abort()

            return


class SchedulerHandler(object):
    """Scheduler messages handler"""

    def get_jobs(self, settings):
        scheduler = self.process.scheduler
        return [ str(job) for job in scheduler.get_jobs() ]

    def reset_task(self, settings):
        TaskResettingThread(self.process, settings).start()
        return 'OK'

    def run_task(self, settings):
        TaskRunnerThread(self.process, settings).start()
        return 'OK'


class SchedulerMessageHandler(ZMQMessageHandler):
    """ZMQ scheduler messages handler"""
    handler = SchedulerHandler


class SchedulerProcess(ZMQProcess):
    """ZMQ scheduler process"""
    scheduler = None
    scheduler_util = None

    def __init__(self, scheduler, handler):
        ZMQProcess.__init__(self, scheduler.zmq_address, handler)
        self.scheduler_path = getPath(scheduler)
        self.scheduler = SchedulerBase()
        if self.scheduler is not None:
            jobs_store = self.jobs_store = ZODBJobsStore(scheduler, self.scheduler)
            if jobs_store is not None:
                self.scheduler.add_jobstore(jobs_store, 'default')
        return

    def run(self):
        if self.scheduler is not None:
            self.scheduler.start()
        ZMQProcess.run(self)
        return

    def restart(self):
        if self.scheduler is not None:
            self.scheduler.stop()
        return