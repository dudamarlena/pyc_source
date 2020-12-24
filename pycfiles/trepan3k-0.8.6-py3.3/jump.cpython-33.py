# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/jump.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2890 bytes
import inspect, os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdproc as Mcmdproc

class JumpCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**jump** *lineno*\n\nSet the next line that will be executed. The line must be within the\nstopped or bottom-most execution frame.'
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
        else:
            if self.proc.curindex + 1 != len(self.proc.stack):
                self.errmsg('You can only jump within the bottom frame')
                return False
            else:
                if self.proc.curframe.f_trace is None:
                    self.errmsg("Sigh - operation can't be done here.")
                    return False
                lineno = self.proc.get_an_int(args[1], ('jump: a line number is required, ' + 'got %s.') % args[1])
                if lineno is None:
                    pass
                return False
            try:
                print(self.proc.curframe.f_trace)
                self.proc.curframe.f_lineno = lineno
                self.proc.stack[self.proc.curindex] = (
                 self.proc.stack[self.proc.curindex][0], lineno)
                Mcmdproc.print_location(self.proc)
            except ValueError as e:
                self.errmsg('jump failed: %s' % e)

            return False


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = JumpCommand(cp)
    print('jump when not running: ', command.run(['jump', '1']))
    command.core.execution_status = 'Running'
    cp.curframe = inspect.currentframe()
    cp.curindex = 0
    cp.stack = Mcmdproc.get_stack(cp.curframe, None, None)
    command.run(['jump', '1'])
    cp.curindex = len(cp.stack) - 1
    command.run(['jump', '1'])