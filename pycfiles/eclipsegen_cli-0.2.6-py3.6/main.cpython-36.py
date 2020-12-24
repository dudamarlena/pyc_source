# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eclipsegen_cli/main.py
# Compiled at: 2020-01-16 04:39:49
# Size of source mod 2**32: 271 bytes
import sys
from eclipsegen_cli.cmd import EclipseGeneratorCLI

def main(*argv, exitAfter=True):
    try:
        if not argv:
            argv = sys.argv
        _, ret = EclipseGeneratorCLI.run(argv=argv, exit=exitAfter)
        return ret
    except KeyboardInterrupt as ex:
        print(ex)