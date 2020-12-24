# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/backtrace.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3917 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import stack as Mstack

class BacktraceCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**backtrace** [*count*]\n\nPrint a stack trace, with the most recent frame at the top.  With a\npositive number, print at most many entries.  With a negative number\nprint the top entries minus that number.\n\nAn arrow indicates the 'current frame'. The current frame determines\nthe context used for many debugger commands such as expression\nevaluation or source-line listing.\n\nExamples:\n---------\n\n   backtrace    # Print a full stack trace\n   backtrace 2  # Print only the top two entries\n   backtrace -1 # Print a stack trace except the initial (least recent) call.\n"
    aliases = ('bt', 'where')
    category = 'stack'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print backtrace of stack frames'

    def run(self, args):
        if len(args) > 1:
            at_most = len(self.proc.stack)
            if at_most == 0:
                self.errmsg('Stack is empty.')
                return False
            else:
                min_value = -at_most + 1
                count = self.proc.get_int(args[1], min_value=min_value, cmdname='backtrace', default=0, at_most=at_most)
                if count is None:
                    pass
                return False
            if count < 0:
                count = at_most - count
            elif 0 == count:
                count = None
        else:
            count = None
        if not self.proc.curframe:
            self.errmsg('No stack.')
            return False
        else:
            Mstack.print_stack_trace(self.proc, count, color=self.settings['highlight'])
            return False


if __name__ == '__main__':
    from trepan.processor import cmdproc
    from trepan import debugger
    d = debugger.Debugger()
    cp = d.core.processor
    command = BacktraceCommand(cp)
    command.run(['backtrace', 'wrong', 'number', 'of', 'args'])

    def nest_me(cp, command, i):
        import inspect
        if i > 1:
            cp.curframe = inspect.currentframe()
            cp.stack, cp.curindex = cmdproc.get_stack(cp.curframe, None, None, cp)
            print('----------')
            command.run(['backtrace'])
            print('----------')
            command.run(['backtrace', '1'])
        else:
            nest_me(cp, command, i + 1)
        return


    def ignore_me(cp, command, i):
        print('==========')
        nest_me(cp, command, 1)
        print('==========')
        cp.core.add_ignore(ignore_me)
        nest_me(cp, command, 1)


    cp.forget()
    command.run(['backtrace'])
    print('----------')
    ignore_me(cp, command, 1)
    command.run(['backtrace', '1'])
    print('----------')
    command.run(['backtrace', '-1'])
    print('----------')
    command.run(['backtrace', '3'])
    print('----------')
    command.run(['backtrace', '-2'])
    print('----------')