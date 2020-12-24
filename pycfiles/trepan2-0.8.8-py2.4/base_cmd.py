# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/base_cmd.py
# Compiled at: 2015-06-12 05:31:55
"""A base class for debugger commands.

This file is the one module in this directory that isn't a real command
and commands.py needs to take care to avoid instantiating this class
and storing it as a list of known debugger commands.
"""
NotImplementedMessage = 'This method must be overriden in a subclass'
import columnize
from pygments.console import colorize
from trepan.lib import format as Mformat
__all__ = [
 'DebuggerCommand']

class DebuggerCommand:
    """Base Class for Debugger commands. We pull in some helper
    functions for command from module cmdfns."""
    __module__ = __name__
    category = 'misc'

    def __init__(self, proc):
        """proc contains the command processor object that this
        command is invoked through.  A debugger field gives access to
        the stack frame and I/O."""
        self.proc = proc
        self.core = proc.core
        self.debugger = proc.debugger
        self.settings = self.debugger.settings

    aliases = ()
    name = 'YourCommandName'

    def columnize_commands(self, commands):
        """List commands arranged in an aligned columns"""
        commands.sort()
        width = self.debugger.settings['width']
        return columnize.columnize(commands, displaywidth=width, lineprefix='    ')

    def confirm(self, msg, default=False):
        """ Convenience short-hand for self.debugger.intf[-1].confirm """
        return self.debugger.intf[(-1)].confirm(msg, default)

    def errmsg(self, msg, opts={}):
        """ Convenience short-hand for self.debugger.intf[-1].errmsg """
        try:
            return self.debugger.intf[(-1)].errmsg(msg)
        except EOFError:
            pass

        return

    def msg(self, msg, opts={}):
        """ Convenience short-hand for self.debugger.intf[-1].msg """
        try:
            return self.debugger.intf[(-1)].msg(msg)
        except EOFError:
            pass

        return

    def msg_nocr(self, msg, opts={}):
        """ Convenience short-hand for self.debugger.intf[-1].msg_nocr """
        try:
            return self.debugger.intf[(-1)].msg_nocr(msg)
        except EOFError:
            pass

        return

    def rst_msg(self, text, opts={}):
        """Convert ReStructuredText and run through msg()"""
        text = Mformat.rst_text(text, 'plain' == self.debugger.settings['highlight'], self.debugger.settings['width'])
        return self.msg(text)

    def run(self, args):
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


if __name__ == '__main__':
    from trepan.processor.command import mock
    (d, cp) = mock.dbg_setup()
    dd = DebuggerCommand(cp)
    dd.msg('hi')
    dd.errmsg("Don't do that")