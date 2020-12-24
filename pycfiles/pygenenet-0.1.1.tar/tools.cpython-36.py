# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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