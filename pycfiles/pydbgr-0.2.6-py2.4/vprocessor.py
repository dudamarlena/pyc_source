# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/vprocessor.py
# Compiled at: 2013-03-24 09:28:50
NotImplementedMessage = 'This method must be overriden in a subclass'
from pygments.console import colorize
from import_relative import import_relative
Mformat = import_relative('lib.format', '..pydbgr')
__all__ = [
 'Processor']

class Processor:
    """A processor is the thing that handles the events that come to
    the debugger.  It has it's own I/O mechanism and a way to handle
    the events.
    """
    __module__ = __name__

    def __init__(self, core_obj):
        self.core = core_obj
        self.debugger = core_obj.debugger

    def errmsg(self, message, opts={}):
        """ Convenience short-hand for self.intf[-1].errmsg """
        if 'plain' != self.debugger.settings['highlight']:
            message = colorize('standout', message)
        return self.intf[(-1)].errmsg(message)

    def msg(self, msg, opts={}):
        """ Convenience short-hand for self.debugger.intf[-1].msg """
        return self.intf[(-1)].msg(msg)

    def msg_nocr(self, msg, opts={}):
        """ Convenience short-hand for self.debugger.intf[-1].msg_nocr """
        return self.intf[(-1)].msg_nocr(msg)

    def event_processor(self, frame, event, arg):
        raise NotImplementedError(NotImplementedMessage)

    def rst_msg(self, text, opts={}):
        """Convert ReStructuredText and run through msg()"""
        text = Mformat.rst_text(text, 'plain' == self.debugger.settings['highlight'], self.debugger.settings['width'])
        return self.msg(text)

    def section(self, message, opts={}):
        if 'plain' != self.settings('highlight'):
            message = colorize('bold', message)
        return self.msg(message, opts)

    def settings(self, setting):
        return self.core.debugger.settings[setting]