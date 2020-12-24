# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/app/main/controller/scheduler_controller.py
# Compiled at: 2020-04-16 16:30:09
# Size of source mod 2**32: 1637 bytes
from flask_restx import Resource
from flask_apscheduler import api as aps_api
from util.dto import SchedulerDto
api = SchedulerDto.api

@api.route('')
class Scheduler(Resource):

    @api.doc('get_scheduler_info')
    def get(self):
        """Gets the scheduler info."""
        return aps_api.get_scheduler_info()


@api.route('/jobs')
class SchedulerJobList(Resource):

    @api.doc('get_jobs')
    def get(self):
        """Gets all scheduled jobs."""
        return aps_api.get_jobs()


@api.route('/jobs/<job_id>')
class SchedulerJob(Resource):

    @api.doc('get_job')
    def get(self, job_id):
        """Gets a job."""
        return aps_api.get_job(job_id)


@api.route('/jobs/<job_id>/pause')
class SchedulerJobPause(Resource):

    @api.doc('pause_job')
    def get(self, job_id):
        """Pauses a job."""
        return aps_api.pause_job(job_id)


@api.route('/jobs/<job_id>/resume')
class SchedulerJobResume(Resource):

    @api.doc('resume_job')
    def get(self, job_id):
        """Resumes a job."""
        return aps_api.resume_job(job_id)


@api.route('/jobs/<job_id>/run')
class SchedulerJobRun(Resource):

    @api.doc('run_job')
    def get(self, job_id):
        """Runs a job."""
        return aps_api.run_job(job_id)