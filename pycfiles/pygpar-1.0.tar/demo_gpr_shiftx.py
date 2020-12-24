# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/demo/demo_gpr_shiftx.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nApplication Example of GP regression\n====================================\n\nThis Example shows the Squared Exponential CF\n(:py:class:`covar.se.SEARDCF`) preprocessed by shiftCF(:py:class`covar.combinators.ShiftCF) and combined with noise\n:py:class:`covar.noise.NoiseISOCF` by summing them up\n(using :py:class:`covar.combinators.SumCF`).\n'
from pygp.covar import se, noise, combinators
from pygp.priors import lnpriors
from pygp.plot import gpr_plot
import logging as LG, numpy.random as random, pylab as PL, scipy as SP
from pygp.gp.gp_base import GP
from pygp.optimize.optimize_base import opt_hyper

def run_demo():
    LG.basicConfig(level=LG.INFO)
    PL.figure()
    random.seed(1)
    n_replicates = 4
    xmin = 1
    xmax = 2.5 * SP.pi
    x1_time_steps = 10
    x2_time_steps = 20
    x1 = SP.zeros(x1_time_steps * n_replicates)
    x2 = SP.zeros(x2_time_steps * n_replicates)
    for i in xrange(n_replicates):
        x1[(i * x1_time_steps):((i + 1) * x1_time_steps)] = SP.linspace(xmin, xmax, x1_time_steps)
        x2[(i * x2_time_steps):((i + 1) * x2_time_steps)] = SP.linspace(xmin, xmax, x2_time_steps)

    C = 2
    sigma1 = 0.15
    sigma2 = 0.15
    n_noises = 1
    b = 0
    y1 = b * x1 + C + 1 * SP.sin(x1)
    y1 += sigma1 * random.randn(y1.shape[0])
    y1 -= y1.mean()
    y2 = b * x2 + C + 1 * SP.sin(x2)
    y2 += sigma2 * random.randn(y2.shape[0])
    y2 -= y2.mean()
    for i in xrange(n_replicates):
        x1[i * x1_time_steps:(i + 1) * x1_time_steps] += 0.7 + i / 2.0
        x2[i * x2_time_steps:(i + 1) * x2_time_steps] -= 0.7 + i / 2.0

    x1 = x1[:, SP.newaxis]
    x2 = x2[:, SP.newaxis]
    x = SP.concatenate((x1, x2), axis=0)
    y = SP.concatenate((y1, y2), axis=0)
    X = SP.linspace(xmin - n_replicates, xmax + n_replicates, 100 * n_replicates)[:, SP.newaxis]
    dim = 1
    replicate_indices = []
    for i, xi in enumerate((x1, x2)):
        for rep in SP.arange(i * n_replicates, (i + 1) * n_replicates):
            replicate_indices.extend(SP.repeat(rep, len(xi) / n_replicates))

    replicate_indices = SP.array(replicate_indices)
    n_replicates = len(SP.unique(replicate_indices))
    logthetaCOVAR = [
     1, 1]
    logthetaCOVAR.extend(SP.repeat(SP.exp(1), n_replicates))
    logthetaCOVAR.extend([sigma1])
    logthetaCOVAR = SP.log(logthetaCOVAR)
    hyperparams = {'covar': logthetaCOVAR}
    SECF = se.SqexpCFARD(dim)
    noiseCF = noise.NoiseCFISO()
    shiftCF = combinators.ShiftCF(SECF, replicate_indices)
    CovFun = combinators.SumCF((shiftCF, noiseCF))
    covar_priors = []
    covar_priors.append([lnpriors.lnGammaExp, [1, 2]])
    for i in range(dim):
        covar_priors.append([lnpriors.lnGammaExp, [1, 1]])

    for i in range(n_replicates):
        covar_priors.append([lnpriors.lnGauss, [0, 0.5]])

    for i in range(n_noises):
        covar_priors.append([lnpriors.lnGammaExp, [1, 1]])

    covar_priors = SP.array(covar_priors)
    priors = {'covar': covar_priors}
    Ifilter = {'covar': SP.ones(n_replicates + 3)}
    gpr = GP(CovFun, x=x, y=y)
    opt_model_params = opt_hyper(gpr, hyperparams, priors=priors, gradcheck=True, Ifilter=Ifilter)[0]
    M, S_glu = gpr.predict(opt_model_params, X)
    T = opt_model_params['covar'][2:2 + n_replicates]
    PL.subplot(212)
    gpr_plot.plot_sausage(X, M, SP.sqrt(S_glu), format_line=dict(alpha=1, color='g', lw=2, ls='-'))
    gpr_plot.plot_training_data(x, y, shift=T, replicate_indices=replicate_indices, draw_arrows=2)
    PL.suptitle('Example for GPTimeShift with simulated data', fontsize=23)
    PL.title('Regression including time shift')
    PL.xlabel('x')
    PL.ylabel('y')
    ylim = PL.ylim()
    gpr = GP(combinators.SumCF((SECF, noiseCF)), x=x, y=y)
    priors = {'covar': covar_priors[[0, 1, -1]]}
    hyperparams = {'covar': logthetaCOVAR[[0, 1, -1]]}
    opt_model_params = opt_hyper(gpr, hyperparams, priors=priors, gradcheck=True)[0]
    PL.subplot(211)
    M, S_glu = gpr.predict(opt_model_params, X)
    gpr_plot.plot_sausage(X, M, SP.sqrt(S_glu), format_line=dict(alpha=1, color='g', lw=2, ls='-'))
    gpr_plot.plot_training_data(x, y, replicate_indices=replicate_indices)
    PL.title('Regression without time shift')
    PL.xlabel('x')
    PL.ylabel('y')
    PL.ylim(ylim)
    PL.subplots_adjust(left=0.1, bottom=0.1, right=0.96, top=0.8, wspace=0.4, hspace=0.4)
    PL.show()


if __name__ == '__main__':
    run_demo()