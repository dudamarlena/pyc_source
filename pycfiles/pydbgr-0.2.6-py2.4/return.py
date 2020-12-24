# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/return.py
# Compiled at: 2013-03-24 01:16:54
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', top_name='pydbgr')
Mfile = import_relative('file', '....lib', 'pydbgr')
Mmisc = import_relative('misc', '....', 'pydbgr')
Mpp = import_relative('pp', '....lib', 'pydbgr')

class InfoReturn(Mbase_subcmd.DebuggerSubcommand):
    """return value

Show the value that is to be returned from a function.  This command
is useful after a 'finish' command or stepping just after a 'return'
statement."""
    __module__ = __name__
    min_abbrev = 1
    need_stack = True
    short_help = 'Show function return value'

    def run(self, args):
        if self.proc.event in ['return', 'exception']:
            val = self.proc.event_arg
            Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg)
        else:
            self.errmsg("Must be in a 'return' or 'exception' event rather than a %s event." % self.proc.event)


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoReturn(i)
    print sub.run([])