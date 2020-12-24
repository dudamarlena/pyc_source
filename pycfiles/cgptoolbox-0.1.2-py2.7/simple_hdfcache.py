# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_hdfcache.py
# Compiled at: 2013-01-14 06:47:43
"""
Cache computations to HDF file for simple genotype-phenotype example.

Here, the line "ph = hdfcache.cache(ph)" is equivalent to the decorator syntax:

.. code-block:: none
   
   @hdfcache.cache
   def ph(...):
       ...

However, cgp.examples.simple.ph is left undecorated so we can illustrate 
different tools for caching and parallelization. 
"""
import os
from tempfile import gettempdir
from cgp.utils.hdfcache import Hdfcache
from cgp.examples.simple import *
if __name__ == '__main__':
    hdfcache = Hdfcache(os.path.join(gettempdir(), 'cgpdemo.h5'))
    ph = hdfcache.cache(ph)
    result = np.concatenate([ ph(gt) for gt in gts ]).view(np.recarray)
    visualize(result)