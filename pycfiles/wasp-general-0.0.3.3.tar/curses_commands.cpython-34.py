# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/cli/curses_commands.py
# Compiled at: 2017-10-28 02:14:54
# Size of source mod 2**32: 2162 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type
from wasp_general.command.command import WCommand
from wasp_general.command.result import WPlainCommandResult
from wasp_general.cli.curses import WCursesConsole

class WExitCommand(WCommand):

    @verify_type(console=WCursesConsole)
    def __init__(self, console):
        WCommand.__init__(self)
        self._WExitCommand__console = console

    def console(self):
        return self._WExitCommand__console

    @verify_type('paranoid', command_tokens=str)
    def match(self, *command_tokens, **command_env):
        return command_tokens == ('exit', ) or command_tokens == ('quit', )

    @verify_type('paranoid', command_tokens=str)
    def _exec(self, *command_tokens, **command_env):
        self._WExitCommand__console.stop()
        return WPlainCommandResult('Exiting...')


class WEmptyCommand(WCommand):

    @verify_type('paranoid', command_tokens=str)
    def match(self, *command_tokens, **command_env):
        return len(command_tokens) == 0

    @verify_type('paranoid', command_tokens=str)
    def _exec(self, *command_tokens, **command_env):
        return WPlainCommandResult('')