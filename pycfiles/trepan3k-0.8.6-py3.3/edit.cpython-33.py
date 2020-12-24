# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/edit.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2858 bytes
import inspect, os
from trepan.processor.command import base_cmd as Mbase_cmd

class EditCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**edit** *position*\n\nEdit specified file or module.\nWith no argument, edits file containing most recent line listed.\n\nSee also:\n---------\n\n`list`\n'
    aliases = ('ed', )
    category = 'files'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Edit specified file or module'

    def run(self, args):
        curframe = self.proc.curframe
        if len(args) == 1:
            if curframe is None:
                self.errmsg('edit: no stack to pick up position from. Use edit FILE:LINE form.')
                return
            filename = curframe.f_code.co_filename
            lineno = curframe.f_lineno
        else:
            if len(args) == 2:
                modfunc, filename, lineno = self.proc.parse_position(args[1])
                if inspect.ismodule(modfunc) and lineno is None and len(args) > 2:
                    val = self.proc.get_an_int(args[1], 'Line number expected, got %s.' % args[1])
                    if val is None:
                        return
                    lineno = val
                elif lineno is None:
                    self.errmsg('edit: no linenumber provided')
                    return
            editor = 'ex'
            if 'EDITOR' in os.environ:
                editor = os.environ['EDITOR']
            if os.path.exists(filename):
                os.system('%s +%d %s' % (editor, lineno, filename))
            else:
                self.errmsg("edit: file %s doesn't exist" % filename)
        return


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    cmd = EditCommand(d.core.processor)
    for c in (['edit'],
     [
      'edit', './edit.py:34'],
     [
      'edit', './noogood.py']):
        cmd.run(c)