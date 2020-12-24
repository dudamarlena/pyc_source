# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/foldFBU.py
# Compiled at: 2018-05-17 07:31:45
import pymc as mc
from numpy import random, dot, array, inf

class fbu(object):
    """A class to perform a MCMC sampling.

    [more detailed description should be added here]

    All configurable parameters are set to some default value, which
    can be changed later on, but before calling the `run` method.
    """

    def __init__(self, data=[], response=[], background={}, backgroundsyst={}, objsyst={'signal': {}, 'background': {}}, lower=[], upper=[], regularization=None, rndseed=-1, verbose=False, name='', monitoring=False):
        self.use_emcee = False
        self.nwalkers = 500
        self.nMCMC = 500000
        self.nBurn = 250000
        self.nThin = 10
        self.lower = lower
        self.upper = upper
        self.prior = 'DiscreteUniform'
        self.priorparams = {}
        self.regularization = regularization
        self.data = data
        self.response = response
        self.background = background
        self.backgroundsyst = backgroundsyst
        self.objsyst = objsyst
        self.systfixsigma = 0.0
        self.rndseed = rndseed
        self.verbose = verbose
        self.name = name
        self.monitoring = monitoring

    def validateinput(self):

        def checklen(list1, list2):
            assert len(list1) == len(list2), 'Input Validation Error: inconstistent size of input'

        responsetruthbins = self.response
        responserecobins = [ row for row in self.response ]
        for list in self.background.values() + responserecobins:
            checklen(self.data, list)

        for list in [self.lower, self.upper]:
            checklen(list, responsetruthbins)

    def fluctuate(self, data):
        random.seed(self.rndseed)
        return random.poisson(data)

    def __call__(self):
        self.validateinput()
        data = self.data
        data = self.fluctuate(data) if self.rndseed >= 0 else data
        backgroundkeys = self.backgroundsyst.keys()
        backgrounds = array([ self.background[key] for key in backgroundkeys ])
        backgroundnormsysts = array([ self.backgroundsyst[key] for key in backgroundkeys
                                    ])
        objsystkeys = self.objsyst['signal'].keys()
        signalobjsysts = array([ self.objsyst['signal'][key] for key in objsystkeys
                               ])
        backgroundobjsysts = array([])
        if len(objsystkeys) > 0 and len(backgroundkeys) > 0:
            backgroundobjsysts = array([ [ self.objsyst['background'][syst][bckg] for syst in objsystkeys ] for bckg in backgroundkeys
                                       ])
        recodim = len(data)
        resmat = self.response
        truthdim = len(resmat)
        import priors
        truth = priors.wrapper(priorname=self.prior, low=self.lower, up=self.upper, other_args=self.priorparams)
        bckgnuisances = []
        for name, err in zip(backgroundkeys, backgroundnormsysts):
            if err < 0.0:
                bckgnuisances.append(mc.Uniform('norm_%s' % name, value=1.0, lower=0.0, upper=3.0))
            else:
                bckgnuisances.append(mc.TruncatedNormal('gaus_%s' % name, value=0.0, mu=0.0, tau=1.0, a=-1.0 / err if err > 0.0 else -inf, b=inf, observed=False if err > 0.0 else True))

        bckgnuisances = mc.Container(bckgnuisances)
        objnuisances = [ mc.Normal('gaus_%s' % name, value=self.systfixsigma, mu=0.0, tau=1.0, observed=True if self.systfixsigma != 0 else False) for name in objsystkeys
                       ]
        objnuisances = mc.Container(objnuisances)
        if self.regularization:
            truthpot = self.regularization.getpotential(truth)

        @mc.deterministic(plot=False)
        def unfold(truth=truth, bckgnuisances=bckgnuisances, objnuisances=objnuisances):
            smearbckg = 1.0
            if len(backgroundobjsysts) > 0:
                smearbckg = smearbckg + dot(objnuisances, backgroundobjsysts)
            smearedbackgrounds = backgrounds * smearbckg
            bckgnormerr = array([ (-1.0 + nuis) / nuis if berr < 0.0 else berr for berr, nuis in zip(backgroundnormsysts, bckgnuisances)
                                ])
            bckg = dot(1.0 + bckgnuisances * bckgnormerr, smearedbackgrounds)
            reco = dot(truth, resmat)
            smear = 1.0 + dot(objnuisances, signalobjsysts)
            out = bckg + reco * smear
            return out

        unfolded = mc.Poisson('unfolded', mu=unfold, value=data, observed=True, size=recodim)
        allnuisances = mc.Container(bckgnuisances + objnuisances)
        modelelements = [unfolded, unfold, truth, allnuisances]
        if self.regularization:
            modelelements += [truthpot]
        model = mc.Model(modelelements)
        if self.use_emcee:
            from emcee_sampler import sample_emcee
            mcmc = sample_emcee(model, nwalkers=self.nwalkers, samples=self.nMCMC / self.nwalkers, burn=self.nBurn / self.nwalkers, thin=self.nThin)
        else:
            map_ = mc.MAP(model)
            map_.fit()
            mcmc = mc.MCMC(model)
            mcmc.use_step_method(mc.AdaptiveMetropolis, truth + allnuisances)
            mcmc.sample(self.nMCMC, burn=self.nBurn, thin=self.nThin)
        self.trace = [ mcmc.trace('truth%d' % bin)[:] for bin in range(truthdim)
                     ]
        self.nuisancestrace = {}
        for name, err in zip(backgroundkeys, backgroundnormsysts):
            if err < 0.0:
                self.nuisancestrace[name] = mcmc.trace('norm_%s' % name)[:]
            if err > 0.0:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s' % name)[:]

        for name in objsystkeys:
            if self.systfixsigma == 0.0:
                self.nuisancestrace[name] = mcmc.trace('gaus_%s' % name)[:]

        if self.monitoring:
            import monitoring
            monitoring.plot(self.name + '_monitoring', data, backgrounds, resmat, self.trace, self.nuisancestrace, self.lower, self.upper)