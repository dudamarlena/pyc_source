# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cray/commands/status.py
# Compiled at: 2020-03-04 04:13:49
# Size of source mod 2**32: 1336 bytes
from cliff.show import ShowOne
import cray.jobs as jobs
import cray.tasks as tasks
import logging

class Status(ShowOne):
    __doc__ = 'Get the current status of a job'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Status, self).get_parser(prog_name)
        parser.add_argument('-j',
          '--job',
          nargs=1,
          required=True,
          help='Job ID',
          type=str,
          dest='job',
          default=None)
        return parser

    def job_status(self, job):
        if not jobs.exists(job):
            raise Exception("Job does not exist or is still being scheduled: '{}'".format(job))
        status = 'Running'
        executed = tasks.count_executed(job)
        total = tasks.count(job)
        scheduled = jobs.scheduled_at(job)
        cancelled_at = jobs.cancelled_at(job)
        if jobs.is_job_cancelled(job):
            status = 'Cancelled'
        if executed == total:
            status = 'Finished'
        return (
         ('# tasks', '# tasks executed', 'status', 'scheduled at', 'cancelled at'),
         (
          total, executed, status, scheduled, cancelled_at))

    def take_action(self, parsed_args):
        return self.job_status(parsed_args.job[0])