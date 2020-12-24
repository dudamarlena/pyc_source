# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/return.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2038 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import pp as Mpp

class InfoReturn(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = "return value\n\nShow the value that is to be returned from a function.  This command\nis useful after a 'finish' command or stepping just after a 'return'\nstatement."
    min_abbrev = 1
    need_stack = True
    short_help = 'Show function return value'

    def run(self, args):
        if self.proc.event in ('return', 'exception'):
            val = self.proc.event_arg
            Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg)
        else:
            self.errmsg("Must be in a 'return' or 'exception' event rather than a %s event." % self.proc.event)


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoReturn(i)
    print(sub.run([]))