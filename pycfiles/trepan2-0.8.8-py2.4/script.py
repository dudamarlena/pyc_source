# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/script.py
# Compiled at: 2015-02-16 15:47:50
"""Module for reading debugger scripts"""
import atexit
from trepan import interface as Minterface, misc as Mmisc
from trepan.inout import scriptin as Mscriptin, output as Moutput

class ScriptInterface(Minterface.DebuggerInterface):
    """Interface when reading debugger scripts"""
    __module__ = __name__
    DEFAULT_INIT_OPTS = {'abort_on_error': True, 'confirm_val': False, 'verbose': False}

    def __init__(self, script_name, out=None, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, self.DEFAULT_INIT_OPTS)
        atexit.register(self.finalize)
        self.script_name = script_name
        self.histfile = None
        self.input_lineno = 0
        self.input = Mscriptin.ScriptInput(script_name)
        self.interactive = False
        self.output = out or Moutput.DebuggerUserOutput()
        self.abort_on_error = get_option('abort_on_error')
        self.default_confirm = get_option('confirm_val')
        self.verbose = get_option('verbose')
        return

    def close(self):
        """ Closes input. (We don't have an output.)"""
        self.input.close()

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done, to make
        sure it's okay. """
        return self.default_confirm

    def errmsg(self, msg, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        if not self.verbose:
            location = '%s:%s: Error in source command file' % (self.script_name, self.input_lineno)
            msg = '%s%s:\n%s%s' % (prefix, location, prefix, msg)
        else:
            msg = '%s%s' % (prefix, msg)
        self.msg(msg)
        if self.abort_on_error:
            raise EOFError

    def finalize(self, last_wishes=None):
        self.close()

    def read_command(self, prompt=''):
        """Script interface to read a command. `prompt' is a parameter for
        compatibilty and is ignored."""
        self.input_lineno += 1
        line = self.readline()
        if self.verbose:
            location = '%s line %s' % (self.script_name, self.input_lineno)
            self.msg('+ %s: %s' % (location, line))
        return line

    def readline(self, prompt=''):
        """Script interface to read a line. `prompt' is a parameter for
        compatibilty and is ignored."""
        return self.input.readline()


if __name__ == '__main__':
    intf = ScriptInterface('script.py')
    line = intf.readline()
    print 'Line read: %s' % line