# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/display.py
# Compiled at: 2015-05-17 09:17:03
from trepan.processor.command import base_subcmd as Mbase_subcmd

class InfoDisplay(Mbase_subcmd.DebuggerSubcommand):
    """**info display**

Show the display expression evaluated when the program stops.

See also:
---------
`display`, `undisplay`"""
    __module__ = __name__
    min_abbrev = 2
    need_stack = True
    short_help = 'Expressions to display when program stops'

    def run(self, args):
        lines = self.proc.display_mgr.all()
        if 0 == len(lines):
            self.errmsg('There are no auto-display expressions now.')
            return
        for line in lines:
            self.msg(line)


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoDisplay(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])
    sub.proc.display_mgr.add(cp.curframe, '/x i')
    sub.proc.display_mgr.add(cp.curframe, 'd')
    sub.run([])