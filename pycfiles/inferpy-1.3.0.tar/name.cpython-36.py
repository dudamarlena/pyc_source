# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/name.py
# Compiled at: 2019-09-03 11:37:11
# Size of source mod 2**32: 580 bytes
from collections import defaultdict
prefixes_count = defaultdict(int)

def generate(prefix):
    """This function is used to generate names based on an incremental counter (global variable in this module)
        dependent on the prefix (staring from 0 index)

        :prefix (`str`): The begining of the random generated name

        :returns: The generated random name
    """
    name = '{}_{}'.format(prefix, prefixes_count[prefix])
    prefixes_count[prefix] = prefixes_count[prefix] + 1
    return name