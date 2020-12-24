# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/continue.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3244 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdbreak as Mcmdbreak

class ContinueCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**continue** [*location*]\n\nLeave the debugger read-eval print loop and continue\nexecution. Subsequent entry to the debugger however may occur via\nbreakpoints or explicit calls, or exceptions.\n\nIf *location* is given, a temporary breakpoint is set at that\nposition before continuing.\n\nExamples:\n---------\n\n    continue          # Continue execution\n    continue 5        # Continue with a one-time breakpoint at line 5\n    continue basename # Go to os.path.basename if we have basename imported\n    continue /usr/lib/python2.7/posixpath.py:110 # Possibly the same as\n                                                 # the above using file\n                                                 # and line number\n\nSee also:\n---------\n\n`step` `jump`, `next`, `finish` and `help syntax location`\n'
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
            func, filename, lineno, condition = Mcmdbreak.parse_break_cmd(self.proc, args)
            if not Mcmdbreak.set_break(self, func, filename, lineno, condition, True, args):
                return False
        self.core.step_events = None
        self.core.step_ignore = -1
        self.proc.continue_running = True
        return True


if __name__ == '__main__':
    import sys
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    cmd = ContinueCommand(d.core.processor)
    cmd.proc.frame = sys._getframe()
    cmd.proc.setup()
    for c in (['continue', 'wrong', 'number', 'of', 'args'],
     [
      'c', '5'],
     [
      'continue', '1+2'],
     [
      'c', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print('Run result: %s' % result)
        print('step_ignore %d, continue_running: %s' % (d.core.step_ignore,
         cmd.continue_running))