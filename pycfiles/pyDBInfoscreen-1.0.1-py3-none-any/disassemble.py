# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/disassemble.py
# Compiled at: 2013-03-22 17:59:25
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mdis = import_relative('disassemble', '...lib', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')

class DisassembleCommand(Mbase_cmd.DebuggerCommand):
    """**disassemble** [*thing*] [[**+**|**-**]*start-line*|**.** [[**+**|**-**]*end-line*|**.**]]

With no argument, disassemble the current frame.  With an integer
start-line, the disassembly is narrowed to show lines starting
at that line number or later; with an end-line number, disassembly
stops when the next line would be greater than that or the end of the
code is hit.

If *start-line* or *end-line is* `.`, `+`, or `-`, the current line number
is used.  If instead it starts with a plus or minus prefix to a
number, then the line number is relative to the current frame number.

With a class, method, function, pyc-file, code or string argument
disassemble that.

**Examples:**

   disassemble    # Possibly lots of stuff dissassembled
   disassemble .  # Disassemble lines starting at current stopping point.
   disassemble +                  # Same as above
   disassemble +0                 # Same as above
   disassemble os.path            # Disassemble all of os.path
   disassemble os.path.normcase   # Disaassemble just method os.path.normcase
   disassemble -3  # Disassemble subtracting 3 from the current line number
   disassemble +3  # Disassemble adding 3 from the current line number
   disassemble 3                  # Disassemble starting from line 3
   disassemble 3 10               # Disassemble lines 3 to 10
   disassemble myprog.pyc         # Disassemble file myprog.pyc
"""
    __module__ = __name__
    aliases = ('disasm', )
    category = 'data'
    min_args = 0
    max_args = 2
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Disassemble Python bytecode'

    def parse_arg(self, arg):
        if arg in ['+', '-', '.']:
            return (self.proc.curframe.f_lineno, True)
        lineno = self.proc.get_int_noerr(arg)
        if lineno is not None:
            if arg[0:1] in ['+', '-']:
                return (lineno + self.proc.curframe.f_lineno, True)
            else:
                return (
                 lineno, False)
        return (None, None)

    def run(self, args):
        start_line = -1
        end_line = None
        relative_pos = False
        if len(args) > 1:
            (start_line, relative_pos) = self.parse_arg(args[1])
            if start_line is None:
                if args[1].endswith('.pyc') and Mfile.readable(args[1]):
                    (magic, moddate, modtime, obj) = Mdis.pyc2code(args[1])
                elif not self.proc.curframe:
                    self.errmsg('No frame selected.')
                    return
                else:
                    try:
                        obj = self.proc.eval(args[1])
                        start_line = -1
                    except:
                        self.errmsg(("Object '%s' is not something we can" + ' disassemble.') % args[1])
                        return

                if len(args) > 2:
                    (start_line, relative_pos) = self.parse_arg(args[2])
                    if start_line is None:
                        self.errmsg = 'Start line should be a number. Got %s.' % args[2]
                        return
                    if len(args) == 4:
                        (end_line, relative_pos) = self.parse_arg(args[3])
                        if end_line is None:
                            self.errmsg = 'End line should be a number. ' + ' Got %s.' % args[3]
                            return
                    elif len(args) > 4:
                        self.errmsg('Expecting 0-3 parameters. Got %d' % len(args) - 1)
                        return
                try:
                    obj = Mcmdfns.get_val(self.proc.curframe, self.errmsg, args[1])
                except:
                    return
                else:
                    Mdis.dis(self.msg, self.msg_nocr, self.section, self.errmsg, obj, start_line=start_line, end_line=end_line, relative_pos=relative_pos)
                    return False
            elif len(args) == 3:
                (end_line, not_used) = self.parse_arg(args[2])
                if end_line is None:
                    self.errmsg = 'End line should be a number. ' + ' Got %s.' % args[2]
                    return
            elif len(args) > 3:
                self.errmsg('Expecting 1-2 line parameters. Got %d.' % len(args) - 1)
                return False
        elif not self.proc.curframe:
            self.errmsg('No frame selected.')
            return
        Mdis.dis(self.msg, self.msg_nocr, self.section, self.errmsg, self.proc.curframe, start_line=start_line, end_line=end_line, relative_pos=relative_pos)
        return False


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    import inspect
    cp.curframe = inspect.currentframe()
    command = DisassembleCommand(cp)
    prefix = '-' * 20 + ' disassemble '
    print prefix + 'cp.errmsg'
    command.run(['dissassemble', 'cp.errmsg'])
    print prefix
    command.run(['disassemble'])
    print prefix + 'me'
    command.run(['disassemble', 'me'])
    print prefix + '+0 2'
    command.run(['disassemble', '+0', '2'])
    print prefix + '+ 2-1'
    command.run(['disassemble', '+', '2-1'])
    print prefix + '- 1'
    command.run(['disassemble', '-', '1'])
    print prefix + '.'
    command.run(['disassemble', '.'])
    print prefix + 'disassemble.pyc 30 70'
    command.run(['disassemble', './disassemble.pyc', '10', '100'])