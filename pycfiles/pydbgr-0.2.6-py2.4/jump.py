# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/jump.py
# Compiled at: 2013-03-23 13:22:34
import inspect, os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdproc = import_relative('cmdproc', '..', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class JumpCommand(Mbase_cmd.DebuggerCommand):
    """**jump** *lineno*

Set the next line that will be executed. The line must be within the
stopped or bottom-most execution frame frame."""
    __module__ = __name__
    aliases = ('j', )
    category = 'running'
    execution_set = ['Running']
    min_args = 1
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Set the next line to be executed'

    def run(self, args):
        if not self.core.is_running():
            return False
        if self.proc.curindex + 1 != len(self.proc.stack):
            self.errmsg('You can only jump within the bottom frame')
            return False
        if self.proc.curframe.f_trace is None:
            self.errmsg("Sigh - operation can't be done here.")
            return False
        lineno = self.proc.get_an_int(args[1], ('jump: a line number is required, ' + 'got %s.') % args[1])
        if lineno is None:
            return False
        try:
            print self.proc.curframe.f_trace
            self.proc.curframe.f_lineno = lineno
            self.proc.stack[self.proc.curindex] = (self.proc.stack[self.proc.curindex][0], lineno)
            Mcmdproc.print_location(self.proc)
        except ValueError:
            (_, e, _) = sys.exc_info()
            self.errmsg('jump failed: %s' % e)

        return False


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = JumpCommand(cp)
    print ('jump when not running: ', command.run(['jump', '1']))
    command.core.execution_status = 'Running'
    cp.curframe = inspect.currentframe()
    cp.curindex = 0
    cp.stack = Mcmdproc.get_stack(cp.curframe, None, None)
    command.run(['jump', '1'])
    cp.curindex = len(cp.stack) - 1
    command.run(['jump', '1'])