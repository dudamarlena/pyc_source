# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\impl.py
# Compiled at: 2019-11-09 02:47:51
# Size of source mod 2**32: 1677 bytes
"""
Generic enhanced terminal command loop.
"""
from __future__ import unicode_literals
from __future__ import print_function
import cmd, logging
from .command import CommandMixin
from .exit import ExitMixin
from .help import HelpMixin
from .macro import MacroMixin
from .message import MessagesMixin
from .run_command import RunCommandsMixin
from .subcommand import SubcommandMixin
from .log_level import LogLevelMixin
from .lang import _
logger = logging.getLogger('enhterm')

class EnhTerm(MessagesMixin, ExitMixin, HelpMixin, CommandMixin, SubcommandMixin, MacroMixin, RunCommandsMixin, LogLevelMixin, cmd.Cmd):
    __doc__ = '\n    Enhanced terminal.\n\n    This is a base class you can use in your project to create a command loop.\n    It includes all mixins defined by the package. If you need fewer\n    mixins use this class as a template.\n    '
    shortcuts = {'x': ('exit', '')}

    def __init__(self, *args, **kwargs):
        self.intro = _('Welcome to the interactive shell.   Type help or ? to list commands.\n')
        super(EnhTerm, self).__init__()
        (cmd.Cmd.__init__)(self, *args, **kwargs)
        self.prompt = '$: '

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.
        """
        should_exit, result = self.cmd_with_result(line)
        MacroMixin.command_hook(self, line)
        return should_exit

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass