# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/aliases.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2613 bytes
import columnize
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowAliases(Mbase_subcmd.DebuggerShowIntSubcommand):
    __doc__ = '**show aliases** [*alias* ...| *]\n\nShow command aliases. If parameters are given a list of all aliases and\nthe command they run are printed. Alternatively one can list specific\nalias names for the commands those specific aliases are attached to.\nIf instead of an alias `*` appears anywhere as an alias then just a list\nof aliases is printed, not what commands they are attached to.\n\nSee also:\n---------\n`alias`\n'
    min_abbrev = len('al')
    short_help = 'Show command aliases'
    run_cmd = False

    def _alias_header(self):
        self.section('Alias      : Command')
        self.msg('%-10s : %s' % ('----------', '-----------'))

    def _alias_line(self, alias):
        self.msg('%-10s : %s' % (alias, self.proc.aliases[alias]))

    def run(self, args):
        aliases = list(self.proc.aliases.keys())
        aliases.sort()
        if len(args) == 0:
            self._alias_header()
            for alias in aliases:
                self._alias_line(alias)

            return
        if '*' in args:
            self.section('Current aliases:')
            self.msg(columnize.columnize(aliases, lineprefix='    '))
        else:
            self._alias_header()
            for alias in args:
                if alias in aliases:
                    self._alias_line(alias)
                else:
                    self.errmsg('%s is not an alias' % alias)

            return


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    sub = Mhelper.demo_run(ShowAliases)
    sub.run(['*'])
    sub.run(['s+', 'n+'])