# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/run/quick.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 54 bytes


def run(config):
    return sum(config['arch_seq'])