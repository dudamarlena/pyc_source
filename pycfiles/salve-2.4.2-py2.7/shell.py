# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/action/shell.py
# Compiled at: 2015-11-06 23:45:35
import subprocess
from salve.action.base import Action
from salve.exceptions import ActionException
from salve.context import ExecutionContext

class ShellAction(Action):
    """
    A ShellAction is one of the basic Action types, used to invoke
    shell subprocesses.
    """

    def __init__(self, command, file_context):
        """
        ShellAction constructor.

        Args:
            @command
            A string that defines the shell command to execute when the
            ShellAction is invoked.
            @file_context
            The FileContext.
        """
        Action.__init__(self, file_context)
        self.cmd = command

    def __str__(self):
        return 'ShellAction(' + str(self.cmd) + ')'

    def execute(self, filesys):
        """
        ShellAction execution.

        Invokes the ShellAction's command, and fails if it returns a
        nonzero exit code, and returns its stdout and stderr.
        """
        ExecutionContext().transition(ExecutionContext.phases.EXECUTION)
        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.wait()
        if process.returncode != 0:
            raise ActionException(str(self) + ' failed with exit code ' + str(process.returncode), self.file_context)
        return process.communicate()