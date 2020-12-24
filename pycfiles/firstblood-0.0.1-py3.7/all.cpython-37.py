# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/all.py
# Compiled at: 2018-10-28 13:45:36
# Size of source mod 2**32: 199 bytes
from . import *
from . import patchAll
from . import unifiedIO as uio
patchAll()
if __name__ == '__main__':
    print('[*] Switching to interactive mode')
    from IPython import embed
    embed()