# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/git.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 649 bytes
import pydoc
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = " Run a git command against this ticketfolder's underlying GIT repo "
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def handle(self, args, folder, **kwargs):
        return (self.cmd)(folder, *self.git_arguments)

    def parse_arguments(self, parser, extra_args):
        args, git_arguments = parser.parse_known_args(extra_args)
        self.git_arguments = git_arguments
        return args

    def main(self, folder, *git_arguments):
        result = (folder.run_git_command)(*git_arguments)
        pydoc.pager(result)
        return result