# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pygenec/tools.py
# Compiled at: 2019-02-12 06:31:54
# Size of source mod 2**32: 464 bytes
from numpy import array

class bcolors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def binarray2int(x):
    cnt = array([2 ** i for i in range(x.shape[1])])
    return array([(cnt * x[i, :]).sum() for i in range(x.shape[0])]).reshape(1, x.shape[0])