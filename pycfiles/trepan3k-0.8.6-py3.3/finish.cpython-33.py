# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/finish.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3220 bytes
import os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import stack as Mstack

class FinishCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**finish** [*level*]\n\nContinue execution until leaving the current function. When *level* is\nspecified, that many frame levels need to be popped. Note that *yield*\nand exceptions raised my reduce the number of stack frames. Also, if a\nthread is switched, we stop ignoring levels.\n\nSee the `break` command if you want to stop at a particular point in a\nprogram.'
    aliases = ('fin', )
    category = 'running'
    execution_set = ['Running']
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Execute until selected stack frame returns'

    def run(self, args):
        if self.proc.stack is None:
            return False
        else:
            if len(args) <= 1:
                levels = 1
            else:
                levels = self.proc.get_int(args[1], default=1, cmdname='finish')
            if levels is None:
                return False
            self.core.step_events = [
             'return']
            self.core.stop_on_finish = True
            self.core.stop_level = Mstack.count_frames(self.proc.frame) - levels
            self.core.last_frame = self.proc.frame
            self.proc.continue_running = True
            return True


if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = FinishCommand(d.core.processor)

    def demo_finish(cmd):
        for c in (['finish', '1'],
         [
          'finish', 'wrong', 'number', 'of', 'args'],
         [
          'finish', '5'],
         [
          'finish', '0*5+1']):
            cmd.continue_running = False
            cmd.proc.stack = [(sys._getframe(0), 14)]
            result = cmd.run(c)
            print('Execute result: %s' % result)
            print('stop_frame %s, continue_running: %s' % (
             cmd.core.stop_frame,
             cmd.continue_running))


    demo_finish(cmd)