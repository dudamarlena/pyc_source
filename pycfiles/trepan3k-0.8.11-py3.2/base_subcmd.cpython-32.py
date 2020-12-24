# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/base_subcmd.py
# Compiled at: 2016-01-13 01:49:32
"""A base class for debugger subcommands.

This file is a module in this directory that isn't a real command
and commands.py needs to take care to avoid instantiating this class
and storing it as a list of known debugger commands.
"""
NotImplementedMessage = 'This method must be overriden in a subclass'
import columnize, re
from pygments.console import colorize

class DebuggerSubcommand:
    """Base Class for Debugger subcommands. We pull in some helper
    functions for command from module cmdfns."""
    in_list = True
    run_cmd = True
    run_in_help = True
    min_abbrev = 1
    min_args = 0
    max_args = None
    need_stack = False

    def __init__(self, cmd):
        """cmd contains the command object that this
        command is invoked through.  A debugger field gives access to
        the stack frame and I/O."""
        self.cmd = cmd
        self.proc = cmd.proc
        self.core = cmd.core
        self.debugger = cmd.debugger
        self.settings = cmd.debugger.settings
        if not hasattr(self, 'short_help'):
            help = self.__doc__.split('\n')
            if len(help) > 0:
                if help[0][0] == '*' and len(help) > 2:
                    self.short_help = help[2]
                else:
                    self.short_help = help[0]
        self.name = self.__module__.split('.')[(-1)]

    def columnize_commands(self, commands):
        """List commands arranged in an aligned columns"""
        commands.sort()
        width = self.debugger.settings['width']
        return columnize.columnize(commands, displaywidth=width, lineprefix='    ')

    def confirm(self, msg, default=False):
        """ Convenience short-hand for self.debugger.intf.confirm """
        return self.debugger.intf[(-1)].confirm(msg, default)

    def errmsg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].errmsg """
        return self.debugger.intf[(-1)].errmsg(msg)

    def msg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg """
        return self.debugger.intf[(-1)].msg(msg)

    def msg_nocr(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg_nocr """
        return self.debugger.intf[(-1)].msg_nocr(msg)

    aliases = ()
    name = 'YourCommandName'

    def rst_msg(self, text):
        """Convenience short-hand for self.proc.rst_msg(text)"""
        return self.proc.rst_msg(text)

    def run(self):
        """ The method that implements the debugger command.
        Help on the command comes from the docstring of this method.
        """
        raise NotImplementedError(NotImplementedMessage)

    def section(self, message, opts={}):
        if 'plain' != self.settings['highlight']:
            message = colorize('bold', message)
        else:
            message += '\n' + '-' * len(message)
        self.msg(message)


from trepan.processor import cmdfns as Mcmdfns
from trepan.lib import complete as Mcomplete

class DebuggerSetBoolSubcommand(DebuggerSubcommand):
    max_args = 1

    def complete(self, prefix):
        result = Mcomplete.complete_token(('on', 'off'), prefix)
        return result

    def run(self, args):
        doc = re.sub('[*]', '', self.short_help).lstrip()
        i = doc.find(' ')
        if i > 0:
            j = doc.find(' ', i + 1)
            if j > 0:
                doc = doc[0:j]
        doc = doc.capitalize().split('\n')[0].rstrip('.')
        Mcmdfns.run_set_bool(self, args)
        Mcmdfns.run_show_bool(self, doc)

    def summary_help(self, subcmd_name, subcmd):
        return self.msg_nocr('%-12s: ' % self.short_help)


class DebuggerShowIntSubcommand(DebuggerSubcommand):
    max_args = 0

    def run(self, args):
        if hasattr(self, 'short_help'):
            short_help = self.short_help
        else:
            short_help = self.__doc__[5:].capitalize()
        Mcmdfns.run_show_int(self, short_help)


class DebuggerShowBoolSubcommand(DebuggerSubcommand):
    max_args = 0

    def run(self, args):
        doc = re.sub('[*]', '', self.short_help)
        doc = doc[5:].capitalize().split('\n')[0].rstrip('.')
        Mcmdfns.run_show_bool(self, doc)


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    dd = DebuggerSubcommand(cp.commands['quit'])