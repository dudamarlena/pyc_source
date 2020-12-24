# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/examples/plot_autoencoder.py
# Compiled at: 2012-10-31 20:07:07
import logging, logging.config
from numpy import *
from util.util import read_mnist, permute_data
from autoencoder_objective import AutoencoderObjective
import phessianfree
from phessianfree import convergence
import scipy.optimize
n_hidden = 40
iters = 30
set_printoptions(precision=4, linewidth=150)
logging.basicConfig(level='DEBUG')
logger = logging.getLogger('opt')
X, d, Xt, dt = read_mnist(partial=False)
ndata = X.shape[0]
X, d = permute_data(X, d)
f = AutoencoderObjective(X, reg=0.0001, n_hidden=n_hidden)
m = f.n_total_weights
rng = random.RandomState(123)
initial_W = asarray(rng.uniform(low=-4.0 * sqrt(6.0 / (f.n_hidden + f.n_visible)), high=4.0 * sqrt(6.0 / (f.n_hidden + f.n_visible)), size=(
 f.n_visible, f.n_hidden)))
bhid = zeros(f.n_hidden)
bvis = zeros(f.n_visible)
x0 = concatenate((bhid, bvis, initial_W.flatten()))
lbfgs_wrapper = convergence.PlottingWrapper(f, 'lbfgs', ndata)
logger.info("Running scipy's lbfgs implementation")
scipy.optimize.fmin_l_bfgs_b(lbfgs_wrapper, copy(x0), m=30, maxfun=iters, disp=5)
phf_cb = convergence.PlottingCallback('phessianfree', ndata)
props = {'subsetVariant': 'lbfgs', 
   'parts': 100, 
   'innerSolveAverage': False, 
   'solveFraction': 0.2, 
   'gradRelErrorBound': 0.1}
logger.info('Running phessianfree with inner lbfgs linear solver')
x, optinfo = phessianfree.optimize(f, x0, ndata, maxiter=20, callback=phf_cb, props=props)
props = {'subsetVariant': 'cg', 
   'parts': 100, 
   'solveFraction': 0.2, 
   'subsetObjective': False}
phf_cb_cg = convergence.PlottingCallback('phessianfree cg', ndata)
logger.info('Running phessianfree with conjugate gradient linear solver')
phf_sgd = convergence.PlottingCallback('SGD', ndata)
x = phessianfree.sgd(f, x0, ndata, maxiter=30, callback=phf_sgd, props={'SGDInitialStep': 30.0, 'SGDStepScale': 0.1})
convergence.plot([lbfgs_wrapper, phf_cb, phf_sgd], [119, 160])