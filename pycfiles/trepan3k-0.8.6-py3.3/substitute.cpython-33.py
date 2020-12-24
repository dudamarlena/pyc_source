# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/substitute.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1834 bytes
import pyficache
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetSubstitute(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = '**set substitute** *from-name* *to-path*\n\nAdd a substitution rule replacing *from-name* into *to-path* in source file names.\nIf a substitution rule was previously set for *from-name*, the old rule\nis replaced by the new one.\n\nSpaces in "filenames" like `<frozen importlib._bootstrap>` messes up our normal shell\ntokenization, so we have added a hack to ignore `<frozen .. >`.\n\nSo, for frozen files like `<frozen importlib._bootstrap>`, `use importlib._bootstrap`\n\nExamples:\n--------\n\n    set substitute importlib._bootstrap /usr/lib/python3.4/importlib/_bootstrap.py\n    set substitute ./gcd.py /tmp/gcd.py\n\n'
    in_list = True
    min_abbrev = len('sub')
    short_help = 'Set filename substitution'

    def run(self, args):
        pyficache.remap_file(args[1], args[0])


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(SetSubstitute)