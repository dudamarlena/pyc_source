# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/continue.py
# Compiled at: 2013-03-17 12:03:19
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mcmdbreak = import_relative('cmdbreak', '..', 'pydbgr')

class ContinueCommand(Mbase_cmd.DebuggerCommand):
    """**continue** [[*file*:]*lineno* | *function*]

Leave the debugger loop and continue execution. Subsequent entry to
the debugger however may occur via breakpoints or explicit calls, or
exceptions.

If a line position or function is given, a temporary breakpoint is set at that
position before continuing.

**EXAMPLES:**

    continue          # Continue execution
    continue 5        # Continue with a one-time breakpoint at line 5
    continue basename # Go to os.path.basename if we have basename imported
    continue /usr/lib/python2.7/posixpath.py:110 # Possibly the same as
                                                 # the above using file
                                                 # and line number
"""
    __module__ = __name__
    category = 'running'
    aliases = ('c', )
    execution_set = ['Running']
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Continue execution of debugged program'

    def run(self, args):
        if len(args) > 1:
            (func, filename, lineno, condition) = Mcmdbreak.parse_break_cmd(self, args[1:])
            if not Mcmdbreak.set_break(self, func, filename, lineno, condition, True, args):
                return False
        self.core.step_events = None
        self.core.step_ignore = -1
        self.proc.continue_running = True
        return True


if __name__ == '__main__':
    import sys
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    cmd = ContinueCommand(d.core.processor)
    cmd.proc.frame = sys._getframe()
    cmd.proc.setup()
    for c in (['continue', 'wrong', 'number', 'of', 'args'], ['c', '5'], ['continue', '1+2'], ['c', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print 'Run result: %s' % result
        print 'step_ignore %d, continue_running: %s' % (d.core.step_ignore, cmd.continue_running)