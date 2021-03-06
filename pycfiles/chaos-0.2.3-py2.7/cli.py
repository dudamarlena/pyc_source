# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/cli.py
# Compiled at: 2015-02-17 11:50:32
import shlex, os
from subprocess import Popen, PIPE, STDOUT

def call_system(command):
    """
        Calls a command using os.system. This method only returns the
        return code of the process. If you want process output, use
        call simple_cli instead.
        """
    return os.system(command)


def call_simple_cli(command, cwd=None, universal_newlines=False, redirect_stderr=False):
    """ Simple wrapper around SimpleCliTool. Simple. """
    return SimpleCliTool()._call_cli(command, cwd, universal_newlines, redirect_stderr)


class SimpleCliTool(object):
    envvars = {}

    def add_env(self, var, value):
        """
                Store a custom environment value internally. This value is used on every
                call to _call_cli.
                """
        self.envvars[var] = value

    def del_env(self, var):
        """
                Delete a custom environment value. This will raise an exception if the
                variable does not exist.
                """
        del self.envvars[var]

    def get_env(self):
        """
                Return the internally stored dict of environment variables.
                """
        return self.envvars

    def _call_cli(self, command, cwd=None, universal_newlines=False, redirect_stderr=False):
        """
                Executes the given command, internally using Popen. The output of
                stdout and stderr are returned as a tuple. The returned tuple looks
                like: (stdout, stderr, returncode)

                Parameters
                ----------
                command: string
                        The command to execute.
                cwd: string
                        Change the working directory of the program to the specified path.
                universal_newlines: boolean
                        Enable the universal_newlines feature of Popen.
                redirect_stderr: boolean
                        If True, redirect stderr into stdout
                """
        command = str(command.encode('utf-8').decode('ascii', 'ignore'))
        env = os.environ.copy()
        env.update(self.envvars)
        stderr = STDOUT if redirect_stderr else PIPE
        proc = Popen(shlex.split(command), stdout=PIPE, stderr=stderr, cwd=cwd, universal_newlines=universal_newlines, env=env)
        stdout, stderr = proc.communicate()
        return (
         stdout, stderr, proc.returncode)