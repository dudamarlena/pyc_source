# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/backtrace.py
# Compiled at: 2019-10-02 10:26:23
import os
from getopt import getopt, GetoptError
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import stack as Mstack

class BacktraceCommand(Mbase_cmd.DebuggerCommand):
    """**backtrace** [*options*] [*count*]

Print backtrace of all stack frames, or innermost *count* frames.

With a negative argument, print outermost -*count* frames.

An arrow indicates the 'current frame'. The current frame determines
the context used for many debugger commands such as expression
evaluation or source-line listing.

*options* are:

   -d | --deparse - show deparsed call position
   -s | --source  - show source code line
   -f | --full    - locals of each frame
   -h | --help    - give this help

Examples:
---------

   backtrace      # Print a full stack trace
   backtrace 2    # Print only the top two entries
   backtrace -1   # Print a stack trace except the initial (least recent) call.
   backtrace -s   # show source lines in listing
   backtrace -d   # show deparsed source lines in listing
   backtrace -f   # show with locals
   backtrace -df  # show with deparsed calls and locals
   backtrace --deparse --full   # same as above

See also:
---------

`frame`, `locals`, `global`, `deparse`, `list`.
"""
    aliases = ('bt', 'where')
    category = 'stack'
    min_args = 0
    max_args = 4
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print backtrace of stack frames'

    def run(self, args):
        try:
            opts, args = getopt(args[1:], 'hfds', 'help deparse full source'.split())
        except GetoptError as err:
            print(str(err))
            return

        bt_opts = {'width': self.settings['width']}
        for o, a in opts:
            if o in ('-h', '--help'):
                self.proc.commands['help'].run(['help', 'backtrace'])
                return
            if o in ('-d', '--deparse'):
                bt_opts['deparse'] = True
            elif o in ('-f', '--full'):
                bt_opts['full'] = True
            elif o in ('-s', '--source'):
                bt_opts['source'] = True
            else:
                self.errmsg("unhandled option '%s'" % o)

        if len(args) > 0:
            at_most = len(self.proc.stack)
            if at_most == 0:
                self.errmsg('Stack is empty.')
                return False
            else:
                min_value = -at_most + 1
                count = self.proc.get_int(args[0], min_value=min_value, cmdname='backtrace', default=0, at_most=at_most)
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
            Mstack.print_stack_trace(self.proc, count, color=self.settings['highlight'], opts=bt_opts)
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