# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/backtrace.py
# Compiled at: 2013-03-11 20:44:27
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mstack = import_relative('stack', '...lib', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class BacktraceCommand(Mbase_cmd.DebuggerCommand):
    """**backtrace** [*count*]

Print a stack trace, with the most recent frame at the top.  With a
positive number, print at most many entries.  With a negative number
print the top entries minus that number.

An arrow indicates the 'current frame'. The current frame determines
the context used for many debugger commands such as expression
evaluation or source-line listing.

**Examples:**

   backtrace    # Print a full stack trace
   backtrace 2  # Print only the top two entries
   backtrace -1 # Print a stack trace except the initial (least recent) call.
"""
    __module__ = __name__
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
            min_value = -at_most + 1
            count = self.proc.get_int(args[1], min_value=min_value, cmdname='backtrace', default=0, at_most=at_most)
            if count is None:
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
        Mstack.print_stack_trace(self.proc, count, color=self.settings['highlight'])
        return False


if __name__ == '__main__':
    cmdproc = import_relative('cmdproc', '..')
    debugger = import_relative('debugger', '...')
    d = debugger.Debugger()
    cp = d.core.processor
    command = BacktraceCommand(cp)
    command.run(['backtrace', 'wrong', 'number', 'of', 'args'])

    def nest_me(cp, command, i):
        import inspect
        if i > 1:
            cp.curframe = inspect.currentframe()
            (cp.stack, cp.curindex) = cmdproc.get_stack(cp.curframe, None, None, cp)
            print '-' * 10
            command.run(['backtrace'])
            print '-' * 10
            command.run(['backtrace', '1'])
        else:
            nest_me(cp, command, i + 1)
        return


    def ignore_me(cp, command, i):
        print '=' * 10
        nest_me(cp, command, 1)
        print '=' * 10
        cp.core.add_ignore(ignore_me)
        nest_me(cp, command, 1)


    cp.forget()
    command.run(['backtrace'])
    print '-' * 10
    ignore_me(cp, command, 1)
    command.run(['backtrace', '1'])
    print '-' * 10
    command.run(['backtrace', '-1'])
    print '-' * 10
    command.run(['backtrace', '3'])
    print '-' * 10
    command.run(['backtrace', '-2'])
    print '-' * 10