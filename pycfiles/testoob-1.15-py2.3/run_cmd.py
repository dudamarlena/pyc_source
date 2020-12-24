# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/run_cmd.py
# Compiled at: 2009-10-07 18:08:46


class SubprocessCommandRunner(object):
    """Run commands with the 'subprocess' module"""
    __module__ = __name__

    def __init__(self):
        try:
            from subprocess import Popen, PIPE
        except ImportError:
            from compatibility.subprocess import Popen, PIPE

        self._Popen = Popen
        self._PIPE = PIPE

    def run(self, args, input=None):
        p = self._Popen(args, stdin=self._PIPE, stdout=self._PIPE, stderr=self._PIPE)
        (stdout, stderr) = p.communicate(input)
        return (stdout, stderr, p.returncode)


class IronPythonCommandRunner(object):
    """Run commands with .NET's API (IronPython currently lacks 'subprocess')"""
    __module__ = __name__

    def __init__(self):
        from System.Diagnostics import Process
        self._Process = Process

    def run(self, args, input=None):
        have_stdin = input is not None
        p = self._Process()
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardInput = have_stdin
        p.StartInfo.RedirectStandardOutput = True
        p.StartInfo.RedirectStandardError = True
        p.StartInfo.FileName = args[0]
        p.StartInfo.Arguments = (' ').join(args[1:])
        p.Start()
        if have_stdin:
            p.StandardInput.Write(input)
        p.WaitForExit()
        stdout = p.StandardOutput.ReadToEnd()
        stderr = p.StandardError.ReadToEnd()
        return (stdout, stderr, p.ExitCode)
        return


def _choose_run_command():
    errors = []
    try:
        return SubprocessCommandRunner().run
    except ImportError, e:
        errors.append(e)

    try:
        return IronPythonCommandRunner().run
    except ImportError, e:
        errors.append(e)

    raise RuntimeError("couldn't find a working command runner", errors)


_run_command_impl = None

def run_command(args, input=None):
    """run_command(args, input=None) -> stdoutstring, stderrstring, returncode
    Runs the command, giving the input if any.
    The command is specified as a list: 'ls -l' would be sent as ['ls', '-l'].
    Returns the standard output and error as strings, and the return code"""
    global _run_command_impl
    if _run_command_impl is None:
        _run_command_impl = _choose_run_command()
    return _run_command_impl(args, input)
    return