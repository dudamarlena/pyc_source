# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/interface/interceptors.py
# Compiled at: 2020-02-01 10:38:26
# Size of source mod 2**32: 112 bytes
from docopt import docopt

def intercept(interface: str) -> dict:
    return docopt(interface)