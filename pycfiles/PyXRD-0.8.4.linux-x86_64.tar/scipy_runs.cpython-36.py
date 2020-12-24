# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/methods/scipy_runs.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2815 bytes
import numpy as np, scipy
from ..refine_method import RefineMethod
from ..refine_method_option import RefineMethodOption
import logging
logger = logging.getLogger(__name__)
MAXFUN = 15000
MAXITER = 15000
IPRINT = 0

class RefineLBFGSBRun(RefineMethod):
    __doc__ = '\n        An implementation of the L BFGS B refinement algorithm.\n    '
    name = 'L BFGS B algorithm'
    description = 'Refinement using the L BFGS B algorithm'
    index = 0
    disabled = False
    maxfun = RefineMethodOption('Maximum # of function calls', MAXFUN, [1, 1000000], int)
    maxiter = RefineMethodOption('Maximum # of iterations', MAXITER, [1, 1000000], int)
    iprint = RefineMethodOption('Output level [-1,0,1]', IPRINT, [-1, 1], int)

    def run(self, refiner, maxfun=MAXFUN, maxiter=MAXITER, iprint=IPRINT, **kwargs):
        """
            Refinement using the L BFGS B algorithm
        """
        solution, residual, d = scipy.optimize.fmin_l_bfgs_b((refiner.get_residual),
          (refiner.history.initial_solution),
          approx_grad=True,
          bounds=(refiner.ranges),
          iprint=iprint,
          epsilon=0.0001,
          callback=(refiner.update),
          maxfun=maxfun,
          maxiter=maxiter)
        refiner.update(solution, residual=residual)
        logger.debug('fmin_l_bfgs_b returned: %s' % d)


class RefineBasinHoppingRun(RefineMethod):
    __doc__ = '\n        An implementation of the Basin Hopping refinement algorithm.\n    '
    name = 'Basin Hopping Algorithm'
    description = 'Refinement using a basin hopping algorithm'
    index = 4
    disabled = False
    niter = RefineMethodOption('Number of iterations', 100, [10, 10000], int)
    T = RefineMethodOption('Temperature criterion', 1.0, [0.0, None], int)
    stepsize = RefineMethodOption('Displacement step size', 0.5, [0.0, None], float)

    def run(self, refiner, niter=100, T=1.0, stepsize=0.5, **kwargs):
        """
            Refinement using a Basin Hopping Algorithm
        """
        vals = scipy.optimize.basinhopping((refiner.get_residual),
          (refiner.history.initial_solution),
          niter=niter,
          T=T,
          stepsize=stepsize,
          minimizer_kwargs={'method':'L-BFGS-B', 
         'bounds':refiner.ranges},
          callback=(lambda s, r, a: refiner.update(s, r)))
        solution = np.asanyarray(vals.x)
        residual = vals.fun
        refiner.update(solution, residual=residual)