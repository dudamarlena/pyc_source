# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/hash_ring/__init__.py
# Compiled at: 2012-12-14 20:14:49
from hash_ring import HashRing
try:
    from memcache_ring import MemcacheRing
except ImportError as e:
    pass