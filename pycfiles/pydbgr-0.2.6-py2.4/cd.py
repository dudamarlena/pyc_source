# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/cd.py
# Compiled at: 2013-03-17 12:03:17
import os, sys
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')

class CDCommand(Mbase_cmd.DebuggerCommand):
    """**cd** *directory*

Set working directory to *directory* for debugger and program
being debugged. """
    __module__ = __name__
    aliases = ('chdir', )
    category = 'files'
    min_args = 1
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Set working directory to DIR for debugger and program being debugged'

    def run(self, args):
        try:
            os.chdir(args[1])
            self.msg('Working directory %s.' % os.getcwd())
        except OSError:
            self.errmsg('cd: %s.' % sys.exc_info()[1])


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    cmd = CDCommand(d.core.processor)
    for c in (['cd', 'wrong', 'number', 'of', 'args'], ['cd', 'foo'], ['cd', '.'], ['cd', '/']):
        cmd.run(c)