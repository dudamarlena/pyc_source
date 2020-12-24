# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/aliases.py
# Compiled at: 2013-03-18 05:57:53
import columnize
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowAliases(Mbase_subcmd.DebuggerShowIntSubcommand):
    """**show aliases** [*alias* ...| *]

Show command aliases. If parameters are given a list of all aliases and
the command they run are printed. Alternatively one can list specific
alias names for the commands those specific aliases are attached to.
If instead of an alias `*` appears anywhere as an alias then just a list
of aliases is printed, not what commands they are attached to.
"""
    __module__ = __name__
    min_abbrev = len('al')
    short_help = 'Show command aliases'
    run_cmd = False

    def _alias_header(self):
        self.section('%-10s : %s' % ('Alias', 'Command'))
        self.msg('%-10s : %s' % ('-' * 10, '-' * 11))

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
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    sub = Mhelper.demo_run(ShowAliases)
    sub.run(['*'])
    sub.run(['s+', 'n+'])