# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_joblib.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = "\nUsing joblib to cache and parallelize the computations in simple.py.\n\nCaching can be conveniently applied using decorator syntax:\n\n.. code-block:: none\n   \n   @mem.cache\n   def f(x):\n       ...\n\nHowever, parallelization won't work with this syntax as of joblib 0.6.3.\n"
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