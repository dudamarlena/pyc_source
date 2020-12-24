# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\run_command.py
# Compiled at: 2019-11-09 02:45:51
# Size of source mod 2**32: 1338 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
from .lang import _
logger = logging.getLogger('enhterm')

class RunCommandsMixin(object):
    __doc__ = '\n    Sequence of commands.\n    '

    def __init__(self, *args, **kwargs):
        (super(RunCommandsMixin, self).__init__)(*args, **kwargs)

    def run_commands(self, commands):
        """
        Run a sequence of commands.

        Line starting with a # character are ignored (comments).
        """
        if isinstance(commands, str):
            commands = commands.split('\n')
        for cmditer in commands:
            if cmditer.strip().startswith('#'):
                continue
            should_exit, result = self.cmd_with_result(cmditer)
            if not result:
                break

    def run_file(self, fpath):
        """Executes a file (expects UTF-8 encoding."""
        with open(fpath, 'r', encoding='utf-8') as (fin):
            return self.run_commands(fin.read())

    args_exec = ['path']

    def do_exec(self, arg):
        """
        Executes the commands in a file.

        Parameters
        ----------

        path : string
            The path to a file to execute.
        """
        self.run_file(arg['path'])