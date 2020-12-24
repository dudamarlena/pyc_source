# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/examples/plot_logistic_regression.py
# Compiled at: 2012-11-01 18:25:25
import logging, logging.config
from numpy import *
import scipy.optimize
from util.util import read_mnist, permute_data
from logistic_objective import LogisticObjective
import phessianfree
from phessianfree import convergence
set_printoptions(precision=4, linewidth=150)
logging.basicConfig(level='DEBUG')
logger = logging.getLogger('opt')
X, d, Xt, dt = read_mnist(partial=False)
ndata = X.shape[0]
m = X.shape[1]
X, d = permute_data(X, d)
f = LogisticObjective(X, d, reg=0.001)
x0 = 0.01 * ones(m)
phf_cb = convergence.PlottingCallback('Conf. Hessian free', ndata)
props = {'gradRelErrorBound': 0.1}
x, optinfo = phessianfree.optimize(f, x0, ndata, maxiter=20, callback=phf_cb, props=props)
hf_cb = convergence.PlottingCallback('Hessian free', ndata)
x, optinfo = phessianfree.optimize(f, x0, ndata, maxiter=14, callback=hf_cb, props={'subsetVariant': 'cg', 
   'subsetObjective': False})
lbfgs_wrapper = convergence.PlottingWrapper(f, 'lbfgs', ndata)
logger.info("Running scipy's lbfgs implementation")
scipy.optimize.fmin_l_bfgs_b(lbfgs_wrapper, x0, m=15, maxfun=30, disp=5)
phf_sgd = convergence.PlottingCallback('SGD', ndata)
x = phessianfree.sgd(f, x0, ndata, maxiter=30, callback=phf_sgd, props={'SGDInitialStep': 30.0, 'SGDStepScale': 0.1})
convergence.plot([lbfgs_wrapper, hf_cb, phf_cb, phf_sgd], [0.355, 0.4])