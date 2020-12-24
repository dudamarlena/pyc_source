# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/unalias.py
# Compiled at: 2013-02-04 07:32:32
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')

class UnaliasCommand(Mbase_cmd.DebuggerCommand):
    """**unalias** *alias-name*

Remove alias *alias-name*

See also 'alias'.
"""
    __module__ = __name__
    category = 'support'
    min_args = 1
    max_args = None
    name = 'unalias'
    need_stack = True
    short_help = 'Remove an alias'

    def run(self, args):
        for arg in args[1:]:
            if arg in self.proc.aliases:
                del self.proc.aliases[arg]
                self.msg('Alias for %s removed.' % arg)
            else:
                self.msg('No alias found for %s' % arg)


if __name__ == '__main__':
    cmdproc = import_relative('cmdproc', '..')
    debugger = import_relative('debugger', '...')
    d = debugger.Debugger()
    cp = d.core.processor
    command = UnaliasCommand(cp)
    command.run(['unalias', 's'])
    command.run(['unalias', 's'])
    command.run(['unalias', 'foo', 'n'])