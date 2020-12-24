# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\examples\simple_ipython_parallel.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nUsing IPython.parallel to parallelize the computations in simple.py.\n\n``ipcluster start`` must be run for this example to work.\n\nParallelization can be conveniently applied using decorator syntax:\n\n.. code-block:: none\n   \n   @lv.parallel()\n   def f(x):\n       ...\n\nHowever, cgp.examples.simple.ph is left undecorated so we can illustrate \ndifferent tools for caching and parallelization. \n'
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