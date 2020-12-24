# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/run/random.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 219 bytes
import random

def run(config):
    random.seed(config.get('seed'))
    if 'arch_seq' in config:
        return sum(config['arch_seq']) + random.random()
    return sum(config.values()) + random.random()