# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_hdfcache.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nCache computations to HDF file for simple genotype-phenotype example.\n\nHere, the line "ph = hdfcache.cache(ph)" is equivalent to the decorator syntax:\n\n.. code-block:: none\n   \n   @hdfcache.cache\n   def ph(...):\n       ...\n\nHowever, cgp.examples.simple.ph is left undecorated so we can illustrate \ndifferent tools for caching and parallelization. \n'
import os
from tempfile import gettempdir
from cgp.utils.hdfcache import Hdfcache
from cgp.examples.simple import *
if __name__ == '__main__':
    hdfcache = Hdfcache(os.path.join(gettempdir(), 'cgpdemo.h5'))
    ph = hdfcache.cache(ph)
    result = np.concatenate([ ph(gt) for gt in gts ]).view(np.recarray)
    visualize(result)