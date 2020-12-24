# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bintraypy_cli/main.py
# Compiled at: 2016-09-20 07:22:50
# Size of source mod 2**32: 256 bytes
import sys
from bintraypy_cli.cmd import BintrayPyCLI

def main(*argv, exitAfter=True):
    try:
        if not argv:
            argv = sys.argv
        _, ret = BintrayPyCLI.run(argv=argv, exit=exitAfter)
        return ret
    except KeyboardInterrupt as ex:
        print(ex)