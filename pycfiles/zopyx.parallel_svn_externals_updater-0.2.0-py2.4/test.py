# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zopyx/parallel_svn_externals_updater/test.py
# Compiled at: 2008-07-05 02:47:33
from processing import Pool

def f(x):
    return x * x


p = Pool(4)
result = p.mapAsync(f, range(10))
print result.get(timeout=1)