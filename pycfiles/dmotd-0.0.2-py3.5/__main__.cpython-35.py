# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmotd/__main__.py
# Compiled at: 2019-02-03 11:53:51
# Size of source mod 2**32: 323 bytes
import sys
from .daemon import DMOTD
if len(sys.argv) != 3:
    print('Unexpected arguments: dmotd <file> <port>')
    sys.exit(1)
daemon = DMOTD(str(sys.argv[1]))
daemon.run(port=int(sys.argv[2]))