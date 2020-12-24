# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_entropy.py
# Compiled at: 2008-02-16 08:01:48
"""This returns the entropy of a probability distribution that
produced a given sample.
"""
import Num, mcmc, mcmc_helper, gpkavg, math, kl_dist

def entropy_probs(p):
    """Entropy of a probability distribution."""
    rv = Num.sum(p * Num.log(p)) / math.log(2)
    return rv


def entropy_vec(p, N=None, F=1.0, Clip=0.01):
    """Entropy of a frequency distribution p.
        Here, we assume that p is counts
        derived from multinomial distributed data;
        they are not normalized to one.
        """
    p = Num.asarray(p, Num.Int)
    if N is None:
        N = p.shape[0] ** 2 * 30
    assert Num.sum(p) > 0
    pstart = (0.5 + p) / Num.sum(0.5 + p)
    pV = 0.1 * Num.identity(p.shape[0]) / float(p.shape[0]) ** 1.5
    xp = mcmc.bootstepper(kl_dist.multinomial_logp, pstart, pV, c=(
     p, F), fixer=kl_dist.multinomial_fixer)
    mcmch = mcmc_helper.stepper(xp)
    mcmch.run_to_bottom()
    mcmch.run_to_ergodic(5.0)
    o = []
    while len(o) < N:
        mcmch.run_to_ergodic(1.0 / math.sqrt(N))
        o.append(entropy_probs(kl_dist.P(xp.prms())))

    avg, sigma = gpkavg.avg(o, None, Clip)
    return (-avg, sigma)


if __name__ == '__main__':
    print entropy_vec([100, 100, 100.0, 100.0])