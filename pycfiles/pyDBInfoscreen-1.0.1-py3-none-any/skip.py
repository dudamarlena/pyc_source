# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/skip.py
# Compiled at: 2013-03-23 13:22:36
import inspect, os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdproc = import_relative('cmdproc', '..', 'pydbgr')
Mbytecode = import_relative('bytecode', '...lib', 'pydbgr')

class SkipCommand(Mbase_cmd.DebuggerCommand):
    """**skip** [*count*]
    
Set the next line that will be executed. The line must be within the
stopped or bottom-most execution frame."""
    __module__ = __name__
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
        if self.proc.curindex + 1 != len(self.proc.stack):
            self.errmsg('You can only skip within the bottom frame.')
            return False
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
            self.errmsg('No next line found')
            return False
        try:
            self.proc.curframe.f_lineno = lineno
            self.proc.stack[self.proc.curindex] = (self.proc.stack[self.proc.curindex][0], lineno)
            Mcmdproc.print_location(self.proc)
        except ValueError:
            (_, e, _) = sys.exc_info()
            self.errmsg('skip failed: %s' % e)

        return False


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = SkipCommand(cp)
    print ('skip when not running: ', command.run(['skip', '1']))
    command.core.execution_status = 'Running'
    cp.curframe = inspect.currentframe()
    cp.curindex = 0
    cp.stack = Mcmdproc.get_stack(cp.curframe, None, None)
    command.run(['skip', '1'])
    cp.curindex = len(cp.stack) - 1
    command.run(['skip', '1'])