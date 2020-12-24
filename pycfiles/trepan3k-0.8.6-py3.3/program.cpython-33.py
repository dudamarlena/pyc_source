# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/program.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3613 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan import misc as Mmisc

class InfoProgram(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = '**info program**\n\nExecution status of the program. Listed are:\n\n* Program name\n\n* Instruction PC\n\n* Reason the program is stopped.\n\nSee also:\n---------\n\n`info line`, `info args`, `info frame`, `info pc`'
    min_abbrev = 2
    max_args = 0
    need_stack = True
    short_help = 'Execution status of the program'

    def run(self, args):
        """Execution status of the program."""
        mainfile = self.core.filename(None)
        if self.core.is_running():
            if mainfile:
                part1 = "Python program '%s' is stopped" % mainfile
            else:
                part1 = 'Program is stopped'
            if self.proc.event:
                msg = 'via a %s event.' % self.proc.event
            else:
                msg = '.'
            self.msg(Mmisc.wrapped_lines(part1, msg, self.settings['width']))
            if self.proc.curframe:
                self.msg('PC offset is %d.' % self.proc.curframe.f_lasti)
            if self.proc.event == 'return':
                val = self.proc.event_arg
                part1 = 'Return value is'
                self.msg(Mmisc.wrapped_lines(part1, self.proc._saferepr(val), self.settings['width']))
            elif self.proc.event == 'exception':
                exc_type, exc_value, exc_tb = self.proc.event_arg
                self.msg('Exception type: %s' % self.proc._saferepr(exc_type))
                if exc_value:
                    self.msg('Exception value: %s' % self.proc._saferepr(exc_value))
            self.msg('It stopped %s.' % self.core.stop_reason)
            if self.proc.event in ('signal', 'exception', 'c_exception'):
                self.msg('Note: we are stopped *after* running the line shown.')
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
    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoProgram(i)
    sub.run([])