# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/cd.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1840 bytes
import os, sys
from trepan.processor.command import base_cmd as Mbase_cmd

class CDCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**cd** *directory*\n\nSet working directory to *directory* for debugger and program\nbeing debugged. '
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
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    cmd = CDCommand(d.core.processor)
    for c in (['cd', 'wrong', 'number', 'of', 'args'],
     [
      'cd', 'foo'],
     [
      'cd', '.'],
     [
      'cd', '/']):
        cmd.run(c)