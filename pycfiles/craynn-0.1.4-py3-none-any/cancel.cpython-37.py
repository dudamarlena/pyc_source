# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cray/commands/cancel.py
# Compiled at: 2020-03-04 04:13:49
# Size of source mod 2**32: 834 bytes
from cliff.command import Command
import cray.jobs as jobs
import logging

class Cancel(Command):
    """Cancel"""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Cancel, self).get_parser(prog_name)
        parser.add_argument('-j',
          '--job', nargs=1, required=True, help='Job ID', type=str, dest='job')
        return parser

    def take_action(self, parsed_args):
        jobID = parsed_args.job[0]
        self.log.debug('JobID={}'.format(jobID))
        if jobs.is_job_cancelled(jobID):
            raise Exception("Already cancelled: '{}'".format(jobID))
        if not jobs.is_job_active(jobID):
            raise Exception("Unknown job: '{}'".format(jobID))
        jobs.cancel_job(jobID)
        self.log.info('Job {} cancelled'.format(jobID))