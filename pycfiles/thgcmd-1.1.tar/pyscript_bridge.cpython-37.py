# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/pyscript_bridge.py
# Compiled at: 2019-07-17 15:13:03
# Size of source mod 2**32: 4465 bytes
"""
Bridges calls made inside of a pyscript with the Cmd2 host app while maintaining a reasonable
degree of isolation between the two
"""
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import Optional
from .utils import namedtuple_with_defaults, StdSim

class CommandResult(namedtuple_with_defaults('CommandResult', ['stdout', 'stderr', 'stop', 'data'])):
    __doc__ = "Encapsulates the results from a thgcmd app command\n\n    Named tuple attributes\n    ----------------------\n    stdout: str - output captured from stdout while this command is executing\n    stderr: str - output captured from stderr while this command is executing. None if no error captured.\n    stop: bool - return value of onecmd_plus_hooks after it runs the given command line.\n    data - possible data populated by the command.\n\n    Any combination of these fields can be used when developing a scripting API for a given command.\n    By default stdout, stderr, and stop will be captured for you. If there is additional command specific data,\n    then write that to thgcmd's last_result member. That becomes the data member of this tuple.\n\n    In some cases, the data member may contain everything needed for a command and storing stdout\n    and stderr might just be a duplication of data that wastes memory. In that case, the StdSim can\n    be told not to store output with its pause_storage member. While this member is True, any output\n    sent to StdSim won't be saved in its buffer.\n\n    The code would look like this:\n        if isinstance(self.stdout, StdSim):\n            self.stdout.pause_storage = True\n\n        if isinstance(sys.stderr, StdSim):\n            sys.stderr.pause_storage = True\n\n    See StdSim class in utils.py for more information\n\n    NOTE: Named tuples are immutable.  So the contents are there for access, not for modification.\n    "

    def __bool__(self) -> bool:
        """Returns True if the command succeeded, otherwise False"""
        if self.data is not None:
            if callable(getattr(self.data, '__bool__', None)):
                return bool(self.data)
        return not self.stderr


class PyscriptBridge(object):
    __doc__ = 'Provides a Python API wrapper for application commands.'

    def __init__(self, cmd2_app):
        self._cmd2_app = cmd2_app
        self.cmd_echo = False
        self.stop = False

    def __dir__(self):
        """Return a custom set of attribute names"""
        attributes = []
        attributes.insert(0, 'cmd_echo')
        return attributes

    def __call__(self, command: str, echo: Optional[bool]=None) -> CommandResult:
        """
        Provide functionality to call application commands by calling PyscriptBridge
        ex: app('help')
        :param command: command line being run
        :param echo: if True, output will be echoed to stdout/stderr while the command runs
                     this temporarily overrides the value of self.cmd_echo
        """
        if echo is None:
            echo = self.cmd_echo
        copy_cmd_stdout = StdSim(self._cmd2_app.stdout, echo)
        copy_cmd_stdout.pause_storage = True
        copy_stderr = StdSim(sys.stderr, echo)
        self._cmd2_app.last_result = None
        stop = False
        try:
            self._cmd2_app.stdout = copy_cmd_stdout
            with redirect_stdout(copy_cmd_stdout):
                with redirect_stderr(copy_stderr):
                    stop = self._cmd2_app.onecmd_plus_hooks(command, pyscript_bridge_call=True)
        finally:
            with self._cmd2_app.sigint_protection:
                self._cmd2_app.stdout = copy_cmd_stdout.inner_stream
                self.stop = stop or self.stop

        result = CommandResult(stdout=(copy_cmd_stdout.getvalue()), stderr=(copy_stderr.getvalue() if copy_stderr.getvalue() else None),
          stop=stop,
          data=(self._cmd2_app.last_result))
        return result