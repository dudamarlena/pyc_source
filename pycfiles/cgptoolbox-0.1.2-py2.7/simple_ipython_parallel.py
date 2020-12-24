# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_ipython_parallel.py
# Compiled at: 2013-01-14 06:47:43
"""
Using IPython.parallel to parallelize the computations in simple.py.

``ipcluster start`` must be run for this example to work.

Parallelization can be conveniently applied using decorator syntax:

.. code-block:: none
   
   @lv.parallel()
   def f(x):
       ...

However, cgp.examples.simple.ph is left undecorated so we can illustrate 
different tools for caching and parallelization. 
"""
from IPython.parallel import Client
from cgp.examples.simple import *
if __name__ == '__main__':
    c = Client()
    lv = c.load_balanced_view()

    @lv.parallel(block=True)
    def ph(gt):
        """Import and computation to be run on engines."""
        from cgp.examples.simple import ph
        rec = ph(gt)
        return (
         rec.view(float), rec.dtype)


    result = [ rec.view(dtype) for rec, dtype in ph.map(gts) ]
    result = np.concatenate(result).view(np.recarray)
    visualize(result)