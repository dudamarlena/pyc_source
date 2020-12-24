# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/undisplay.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2716 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete

class UndisplayCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**undisplay** *display-number*...\n\nCancel some expressions to be displayed when program stops.\nArguments are the code numbers of the expressions to stop displaying.\n\nNo argument cancels all automatic-display expressions and is\nthe same as `delete display`.\n\nSee also:\n---------\n\n`info display` to see current list of code numbers.\n'
    aliases = ('und', )
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Cancel some expressions to be displayed when program stops'

    def complete(self, prefix):
        completions = [str(disp.number) for disp in self.proc.display_mgr.list]
        return Mcomplete.complete_token(completions, prefix)

    def run(self, args):
        if len(args) == 1:
            self.proc.display_mgr.clear()
            return
        else:
            for i in args[1:]:
                i = self.proc.get_an_int(i, '%r must be a display number' % i)
                if i is not None:
                    if not self.proc.display_mgr.delete_index(i):
                        self.errmsg('No display number %d.' % i)
                        return
                    continue

            return False


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    from trepan.processor import cmdproc as Mcmdproc
    import inspect
    d = Mdebugger.Trepan()
    cp = d.core.processor
    command = UndisplayCommand(d.core.processor)
    cp.curframe = inspect.currentframe()
    cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    command.run(['undisplay', 'z'])
    command.run(['undisplay', '1', '10'])