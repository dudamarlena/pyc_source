# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/unalias.py
# Compiled at: 2015-04-05 20:36:11
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete

class UnaliasCommand(Mbase_cmd.DebuggerCommand):
    """**unalias** *alias-name*

Remove alias *alias-name*

See also:
---------

'alias'
"""
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