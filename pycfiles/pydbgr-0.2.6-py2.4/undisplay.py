# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/undisplay.py
# Compiled at: 2013-03-17 00:39:16
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')

class UndisplayCommand(Mbase_cmd.DebuggerCommand):
    """**undisplay** *display-number*...

Cancel some expressions to be displayed when program stops.
Arguments are the code numbers of the expressions to stop displaying.

No argument cancels all automatic-display expressions and is
the same as `delete display`.

Use `info display` to see current list of code numbers.
"""
    __module__ = __name__
    aliases = ('und', )
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Cancel some expressions to be displayed when program stops'

    def run(self, args):
        if len(args) == 1:
            self.proc.display_mgr.clear()
            return
        for i in args[1:]:
            i = self.proc.get_an_int(i, '%r must be a display number' % i)
            if i is not None:
                if not self.proc.display_mgr.delete_index(i):
                    self.errmsg('No display number %d.' % i)
                    return

        return False


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    import inspect
    Mcmdproc = import_relative('cmdproc', '..')
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    cp = d.core.processor
    command = UndisplayCommand(d.core.processor)
    cp.curframe = inspect.currentframe()
    (cp.stack, cp.curindex) = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    command.run(['undisplay', 'z'])
    command.run(['undisplay', '1', '10'])