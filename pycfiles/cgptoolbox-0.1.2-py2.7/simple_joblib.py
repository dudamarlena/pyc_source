# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_joblib.py
# Compiled at: 2013-01-14 06:47:43
"""
Using joblib to cache and parallelize the computations in simple.py.

Caching can be conveniently applied using decorator syntax:

.. code-block:: none
   
   @mem.cache
   def f(x):
       ...

However, parallelization won't work with this syntax as of joblib 0.6.3.
"""
import os
from tempfile import gettempdir
from multiprocessing import cpu_count
from joblib import Parallel, delayed, Memory
from cgp.examples.simple import *
if __name__ == '__main__':
    cachedir = os.path.join(gettempdir(), 'simple_joblib')
    mem = Memory(cachedir)
    parallel = Parallel(n_jobs=cpu_count())
    _ph = delayed(mem.cache(ph))
    result = np.concatenate(parallel(_ph(gt) for gt in gts)).view(np.recarray)
    visualize(result)