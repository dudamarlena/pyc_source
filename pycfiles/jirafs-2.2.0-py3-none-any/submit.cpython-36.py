# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/submit.py
# Compiled at: 2019-03-11 23:04:44
# Size of source mod 2**32: 788 bytes
from jirafs.plugin import CommandPlugin
from jirafs.utils import run_command_method_with_kwargs

class Command(CommandPlugin):
    __doc__ = 'Commit current changes, push changes to JIRA, and pull changes'
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def add_arguments(self, parser):
        parser.add_argument('-m',
          '--message', dest='message', default='Untitled')

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, args.message)

    def main(self, folder, message):
        commit_result = run_command_method_with_kwargs('commit',
          folder=folder, message=message)
        push_result = run_command_method_with_kwargs('push',
          folder=folder)
        return (
         commit_result, push_result)