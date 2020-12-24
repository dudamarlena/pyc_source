# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/base_subcmd.py
# Compiled at: 2013-03-18 06:00:55
__doc__ = "A base class for debugger subcommands.\n\nThis file is a module in this directory that isn't a real command\nand commands.py needs to take care to avoid instantiating this class\nand storing it as a list of known debugger commands.\n"
NotImplementedMessage = 'This method must be overriden in a subclass'
import columnize, re
from pygments.console import colorize

class DebuggerSubcommand:
    """Base Class for Debugger subcommands. We pull in some helper
    functions for command from module cmdfns."""
    __module__ = __name__
    in_list = True
    run_cmd = True
    run_in_help = True
    min_abbrev = 1
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
            self.short_help = self.__doc__.split('\n')[0]
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

    aliases = ('alias1', 'alias2..')
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
        self.msg(message)


from import_relative import import_relative
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class DebuggerSetBoolSubcommand(DebuggerSubcommand):
    __module__ = __name__

    def run(self, args):
        doc = re.sub('[*]', '', self.__doc__).lstrip()
        doc = doc.capitalize().split('\n')[0].rstrip('.')
        Mcmdfns.run_set_bool(self, args)
        Mcmdfns.run_show_bool(self, doc)

    def summary_help(self, subcmd_name, subcmd):
        return self.msg_nocr('%-12s: ' % self.short_help)


class DebuggerShowIntSubcommand(DebuggerSubcommand):
    __module__ = __name__

    def run(self, args):
        if hasattr(self, 'short_help'):
            short_help = self.short_help
        else:
            short_help = self.__doc__[5:].capitalize()
        Mcmdfns.run_show_int(self, short_help)


class DebuggerShowBoolSubcommand(DebuggerSubcommand):
    __module__ = __name__

    def run(self, args):
        doc = re.sub('[*]', '', self.__doc__)
        doc = doc[5:].capitalize().split('\n')[0].rstrip('.')
        Mcmdfns.run_show_bool(self, doc)


if __name__ == '__main__':
    from import_relative import import_relative
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    dd = DebuggerSubcommand(cp.commands['quit'])