# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/unalias.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1924 bytes
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete

class UnaliasCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**unalias** *alias-name*\n\nRemove alias *alias-name*\n\nSee also:\n---------\n\n'alias'\n"
    category = 'support'
    min_args = 1
    max_args = None
    name = 'unalias'
    need_stack = True
    short_help = 'Remove an alias'

    def complete(self, prefix):
        return Mcomplete.complete_token(self.proc.aliases.keys(), prefix)

    def run(self, args):
        for arg in args[1:]:
            if arg in self.proc.aliases:
                del self.proc.aliases[arg]
                self.msg('Alias for %s removed.' % arg)
            else:
                self.msg('No alias found for %s' % arg)


if __name__ == '__main__':
    from trepan import debugger
    d = debugger.Trepan()
    cp = d.core.processor
    command = UnaliasCommand(cp)
    command.run(['unalias', 's'])
    command.run(['unalias', 's'])
    command.run(['unalias', 'foo', 'n'])
    print(command.complete(''))