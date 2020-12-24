# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/skip.py
# Compiled at: 2015-06-03 13:32:55
import inspect, os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdproc as Mcmdproc
from trepan.lib import bytecode as Mbytecode

class SkipCommand(Mbase_cmd.DebuggerCommand):
    """**skip** [*count*]

Set the next line that will be executed. The line must be within the
stopped or bottom-most execution frame.

See also:
---------

`next`, `step`, `jump`, `continue`, `return` and
`finish` for other ways to progress execution.
"""
    aliases = ('sk', )
    category = 'running'
    execution_set = ['Running']
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Skip lines to be executed'

    def run(self, args):
        if not self.core.is_running():
            return False
        else:
            if self.proc.curindex + 1 != len(self.proc.stack):
                self.errmsg('You can only skip within the bottom frame.')
                return False
            else:
                if self.proc.curframe.f_trace is None:
                    self.errmsg("Sigh - operation can't be done here.")
                    return False
                if len(args) == 1:
                    count = 1
                else:
                    msg = 'skip: expecting a number, got %s.' % args[1]
                    count = self.proc.get_an_int(args[1], msg)
                co = self.proc.curframe.f_code
                offset = self.proc.curframe.f_lasti
                if count is None:
                    return False
                lineno = Mbytecode.next_linestart(co, offset, count)
                if lineno < 0:
                    pass
                self.errmsg('No next line found')
                return False
            try:
                self.proc.curframe.f_lineno = lineno
                self.proc.stack[self.proc.curindex] = (
                 self.proc.stack[self.proc.curindex][0], lineno)
                Mcmdproc.print_location(self.proc)
            except ValueError as e:
                self.errmsg('skip failed: %s' % e)

            return False


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = SkipCommand(cp)
    print('skip when not running: ', command.run(['skip', '1']))
    command.core.execution_status = 'Running'
    cp.curframe = inspect.currentframe()
    cp.curindex = 0
    cp.stack = Mcmdproc.get_stack(cp.curframe, None, None)
    command.run(['skip', '1'])
    cp.curindex = len(cp.stack) - 1
    command.run(['skip', '1'])