# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/unalias.py
# Compiled at: 2015-02-16 15:47:50
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete

class UnaliasCommand(Mbase_cmd.DebuggerCommand):
    """**unalias** *alias-name*

Remove alias *alias-name*

See also:
---------

'alias'
"""
    __module__ = __name__
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
    d = debugger.Debugger()
    cp = d.core.processor
    command = UnaliasCommand(cp)
    command.run(['unalias', 's'])
    command.run(['unalias', 's'])
    command.run(['unalias', 'foo', 'n'])
    print command.complete('')