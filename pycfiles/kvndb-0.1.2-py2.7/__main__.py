# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvndb/__main__.py
# Compiled at: 2016-11-13 08:39:55
"""the __main__ script can be invoked by python."""
import sys
from . import runner
if __name__ == '__main__':
    runner.run(sys.argv[1:])