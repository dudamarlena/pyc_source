# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/display.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3745 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class DisplayCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**display** [*format*] *expression*\n\nPrint value of expression *expression* each time the program stops.\n*format* may be used before *expression* and may be one of `/c` for\nchar, `/x` for hex, `/o` for octal, `/f` for float or `/s` for string.\n\nFor now, display expressions are only evaluated when in the same\ncode as the frame that was in effect when the display expression\nwas set.  This is a departure from gdb and we may allow for more\nflexibility in the future to specify whether this should be the\ncase or not.\n\nWith no argument, evaluate and display all currently requested\nauto-display expressions.  Use `undisplay` to cancel display\nrequests previously made.'
    category = 'data'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Display expressions when entering debugger'
    format_specs = ('/c', '/x', '/o', '/f', '/s')

    def complete(self, prefix):
        return DisplayCommand.format_specs + Mcomplete.complete_expression(self, prefix)

    def run_eval_display(self, args=None):
        for line in self.proc.display_mgr.display(self.proc.curframe):
            self.msg(line)

    def run(self, args):
        if len(args) == 1:
            self.run_eval_display(self)
        else:
            if args[1] in DisplayCommand.format_specs:
                if len(args) == 2:
                    self.errmsg('Expecting an expression after the format')
                    return
                format = args[1]
                expr = ' '.join(args[2:])
            else:
                format = None
                expr = ' '.join(args[1:])
            dp = self.proc.display_mgr.add(self.proc.curframe, expr, format)
            if dp is None:
                self.errmsg('Error evaluating "%s" in the current frame' % expr)
                return
            self.msg(dp.format(show_enabled=False))
            self.proc.add_preloop_hook(self.run_eval_display)
            self.msg(dp.to_s(self.proc.curframe))
        return False


if __name__ == '__main__':
    from trepan.processor import cmdproc as Mcmdproc
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    import inspect
    d = Mdebugger.Trepan()
    cp = d.core.processor
    command = DisplayCommand(d.core.processor)
    cp.curframe = inspect.currentframe()
    cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    command.run(['display'])
    command.run(['display', '/x', '10'])
    command.run(['display', 'd'])
    print('====================')
    command.run(['display'])