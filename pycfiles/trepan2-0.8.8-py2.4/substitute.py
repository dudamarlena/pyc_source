# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/substitute.py
# Compiled at: 2018-06-25 10:54:33
import pyficache
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetSubstitute(Mbase_subcmd.DebuggerSubcommand):
    """**set substitute** *from-name* *to-path*

Add a substitution rule replacing *from-name* into *to-path* in source file names.
If a substitution rule was previously set for *from-name*, the old rule
is replaced by the new one.

Spaces in "filenames" like `<frozen importlib._bootstrap>` messes up our normal shell
tokenization, so we have added a hack to ignore `<frozen .. >`.

So, for frozen files like `<frozen importlib._bootstrap>`, `use importlib._bootstrap`

Examples:
---------

    set substitute importlib._bootstrap /usr/lib/python3.4/importlib/_bootstrap.py
    set substitute ./gcd.py /tmp/gcd.py

"""
    __module__ = __name__
    in_list = True
    min_abbrev = len('sub')
    short_help = 'Set filename substitution'

    def run(self, args):
        pyficache.remap_file(args[1], args[0])


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(SetSubstitute)