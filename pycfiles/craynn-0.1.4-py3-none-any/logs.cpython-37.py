# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cray/commands/logs.py
# Compiled at: 2020-03-04 04:13:49
# Size of source mod 2**32: 1048 bytes
from cliff.command import Command
import cray.tasks as tasks
import logging, sys

class Logs(Command):
    """Logs"""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('-j',
          '--job', nargs=1, required=True, help='Job ID', type=str, dest='job')
        parser.add_argument('-t',
          '--task',
          nargs=1,
          required=True,
          help='Task ID',
          type=str,
          dest='task')
        return parser

    def take_action(self, parsed_args):
        jobID = parsed_args.job[0]
        taskID = parsed_args.task[0]
        self.log.debug('JobID={} Task={}'.format(jobID, taskID))
        if not tasks.has_executed(jobID, taskID):
            raise Exception('Task {} has not been executed'.format(taskID))
        logs = tasks.logs(jobID, taskID)
        print(logs['out'])
        print((logs['err']), file=(sys.stderr))