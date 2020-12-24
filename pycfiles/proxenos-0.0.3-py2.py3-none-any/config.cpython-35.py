# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/config.py
# Compiled at: 2017-01-22 17:42:46
# Size of source mod 2**32: 477 bytes
"""Provides configuration and configuration defaults."""
from __future__ import absolute_import
import biome
__all__ = ('env', 'mmh_seed', 'mmh_optimize', 'prf', 'siphash_key')
env = biome.proxenos
mmh_seed = env.get_int('mmh_seed', 0)
mmh_optimize = env.get('mmh_optimize', 'auto').lower()
prf = env.get('prf', default='siphash').upper()
siphash_key = env.get('siphash_key', default=b'\xd9\x06\xb0z\x88\x13\x15\xce0\x88G\xa8\xc4\xdei\xc6')