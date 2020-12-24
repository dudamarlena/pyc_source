# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/anaconda3/envs/tbb/lib/python3.8/site-packages/scrapy_redis_bloomfilter/picklecompat.py
# Compiled at: 2019-11-26 21:39:54
# Size of source mod 2**32: 242 bytes
"""A pickle wrapper module with protocol=-1 by default."""
try:
    import cPickle as pickle
except ImportError:
    import pickle
else:

    def loads(s):
        return pickle.loads(s)


    def dumps(obj):
        return pickle.dumps(obj, protocol=(-1))