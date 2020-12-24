# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/style.py
# Compiled at: 2018-06-25 10:54:33
from pygments.styles import STYLE_MAP
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import complete as Mcomplete
style_names = sorted(list(STYLE_MAP.keys()))

def complete(self, prefix):
    return Mcomplete.complete_token(style_names)


class ShowStyle(Mbase_subcmd.DebuggerSubcommand):
    """**show style* *pygments-style*

Show the pygments style used in formatting 256-color terminal text.

See also:
---------

`set style`, `show highlight`
"""
    __module__ = __name__
    in_list = True
    min_abbrev = len('sty')
    short_help = 'Set the pygments style'

    def run(self, args):
        if len(args) != 0:
            self.errmsg('Expecting no args')
            return
        style = self.debugger.settings[self.name]
        if style:
            self.msg('Pygments style is %s' % style)
        else:
            self.msg('Pygments style not set')


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    sub = Mhelper.demo_run(ShowStyle)
    d = sub.proc.debugger
    sub.run([])