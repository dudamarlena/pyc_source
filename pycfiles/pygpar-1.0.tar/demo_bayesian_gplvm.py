# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/demo/demo_bayesian_gplvm.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nCreated on 5 Apr 2012\n\n@author: maxz\n'
from pygp.covar import linear, combinators, noise, bias, se
from pygp.gp.bayesian_gplvm import mean_id, vars_id, ivar_id
from pygp.gp import bayesian_gplvm
import numpy
from pygp.optimize.optimize_base import opt_hyper
import copy, pylab

def random_inputs(N, M, Qlearn, D, covar, noise=0.5, Qreal=None):
    if Qreal is None:
        Qreal = max(1, Qlearn / 4)
    x = numpy.linspace(0, 2 * numpy.pi, N)
    signals = [lambda x: numpy.sin(x)]
    signals = numpy.array(map(lambda f: f(x), signals)).T
    inputs = numpy.zeros((N, Qlearn))
    inputs[:, :signals.shape[1]] = signals
    inputs += 0.3 * numpy.random.randn(*inputs.shape)
    W = 1 + 0.3 * numpy.random.randn(Qlearn, D)
    Y = numpy.dot(inputs, W)
    Y += noise * numpy.random.randn(N, D)
    mean = numpy.random.randn(*inputs.shape) + inputs
    variance = 0.5 * numpy.ones(mean.shape)
    inducing_variables = numpy.random.rand(M, Qlearn) * 2 * numpy.pi
    hyperparams = {'covar': numpy.log(numpy.sqrt(numpy.repeat(0.5, covar.get_number_of_parameters()))), 'beta': numpy.array([0.5]), 
       mean_id: mean, 
       vars_id: numpy.log(numpy.sqrt(variance)), 
       ivar_id: inducing_variables}
    return (
     hyperparams, inputs, Y)


if __name__ == '__main__':
    pylab.ion()
    pylab.close('all')
    smaller = []
    n_runs = 1
    for i in xrange(n_runs):
        N = 45
        Qreal = 2
        M = Qreal + 1
        Qlearn = 6
        D = 20
        lin = linear.LinearCFPsiStat(Qlearn)
        noi = noise.NoiseCFISOPsiStat()
        bia = bias.BiasCFPsiStat()
        covar = combinators.SumCFPsiStat((lin, bia, noi))
        hyperparams, signals, Y = random_inputs(N, M, Qlearn, D, covar, Qreal=Qreal)
        g = bayesian_gplvm.BayesianGPLVM(y=Y, covar_func=covar, gplvm_dimensions=None, n_inducing_variables=M)
        skeys = numpy.sort(hyperparams.keys())
        param_struct = dict([ (name, hyperparams[name].shape) for name in skeys ])
        bounds = {}
        hyper_for_optimizing = copy.deepcopy(hyperparams)
        opt_hyperparams, opt_lml = opt_hyper(g, hyper_for_optimizing, bounds=bounds, maxiter=10000, messages=True)
        g.plot(opt_hyperparams, marker='x', color='b')
        Ystar_mean, Ystar_variance = g.predict(opt_hyperparams, opt_hyperparams[mean_id])
        pylab.figure()
        pylab.subplot(121)
        pylab.imshow(numpy.dot(signals, numpy.ones((Qlearn, D))), aspect='auto', cmap='jet', interpolation='nearest')
        pylab.title('Noise Free Training Outputs')
        pylab.subplot(122)
        pylab.imshow(Ystar_mean, aspect='auto', cmap='jet', interpolation='nearest')
        pylab.title('Predicted Training Outputs')