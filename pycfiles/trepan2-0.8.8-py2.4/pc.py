# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/pc.py
# Compiled at: 2017-08-01 13:58:52
import inspect
from dis import findlinestarts
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib.disassemble import disassemble_bytes
from trepan import misc as Mmisc

class InfoPC(Mbase_subcmd.DebuggerSubcommand):
    """**info pc**

List the current program counter or bytecode offset,
and disassemble the instructions around that.

See also:
---------

`info line`, `info program`
"""
    __module__ = __name__
    min_abbrev = 2
    max_args = 0
    need_stack = True
    short_help = 'Show Program Counter or Instruction Offset information'

    def run(self, args):
        """Program counter."""
        mainfile = self.core.filename(None)
        if self.core.is_running():
            curframe = self.proc.curframe
            if curframe:
                line_no = inspect.getlineno(curframe)
                offset = curframe.f_lasti
                self.msg('PC offset is %d.' % offset)
                offset = max(offset, 0)
                code = curframe.f_code
                co_code = code.co_code
                disassemble_bytes(self.msg, self.msg_nocr, co_code, offset, line_no, line_no - 1, line_no + 1, constants=code.co_consts, cells=code.co_cellvars, varnames=code.co_varnames, freevars=code.co_freevars, linestarts=dict(findlinestarts(code)), end_offset=offset + 10)
        else:
            if mainfile:
                part1 = "Python program '%s'" % mainfile
                msg = 'is not currently running. '
                self.msg(Mmisc.wrapped_lines(part1, msg, self.settings['width']))
            else:
                self.msg('No Python program is currently running.')
            self.msg(self.core.execution_status)
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoPC(i)
    sub.run([])