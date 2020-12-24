# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/program.py
# Compiled at: 2013-03-24 01:16:45
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..')
Mmisc = import_relative('misc', '....', 'pydbgr')

class InfoProgram(Mbase_subcmd.DebuggerSubcommand):
    """Execution status of the program."""
    __module__ = __name__
    min_abbrev = 1
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
                (exc_type, exc_value, exc_tb) = self.proc.event_arg
                self.msg('Exception type: %s' % self.proc._saferepr(exc_type))
                if exc_value:
                    self.msg('Exception value: %s' % self.proc._saferepr(exc_value))
            self.msg('It stopped %s.' % self.core.stop_reason)
            if self.proc.event in ['signal', 'exception', 'c_exception']:
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
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoProgram(i)
    sub.run([])