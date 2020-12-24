# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/bayesiantests.py
# Compiled at: 2019-02-25 14:04:49
# Size of source mod 2**32: 17686 bytes
import numpy as np, numpy.matlib
LEFT, ROPE, RIGHT = range(3)

def correlated_ttest_MC(x, rope, runs=1, nsamples=50000):
    """
    See correlated_ttest module for explanations
    """
    if x.ndim == 2:
        x = x[:, 1] - x[:, 0]
    diff = x
    n = len(diff)
    nfolds = n / runs
    x = np.mean(diff)
    var = np.var(diff, ddof=1) * (1 / n + 1 / (nfolds - 1))
    if var == 0:
        return (
         int(x < rope), int(-rope <= x <= rope), int(rope < x))
    return x + np.sqrt(var) * np.random.standard_t(n - 1, nsamples)


def correlated_ttest(x, rope, runs=1, verbose=False, names=('C1', 'C2')):
    import scipy.stats as stats
    if x.ndim == 2:
        x = x[:, 1] - x[:, 0]
    diff = x
    n = len(diff)
    nfolds = n / runs
    x = np.mean(diff)
    var = np.var(diff, ddof=1) * (1 / n + 1 / (nfolds - 1))
    if var == 0:
        return (
         int(x < rope), int(-rope <= x <= rope), int(rope < x))
    pr = 1 - stats.t.cdf(rope, n - 1, x, np.sqrt(var))
    pl = stats.t.cdf(-rope, n - 1, x, np.sqrt(var))
    pe = 1 - pl - pr
    if verbose:
        print('P({c1} > {c2}) = {pl}, P(rope) = {pe}, P({c2} > {c1}) = {pr}'.format(c1=(names[0]),
          c2=(names[1]),
          pl=pl,
          pe=pe,
          pr=pr))
    return (
     pl, pe, pr)


def signtest_MC(x, rope, prior_strength=1, prior_place=ROPE, nsamples=50000):
    """
    Args:
        x (array): a vector of differences or a 2d array with pairs of scores.
        rope (float): the width of the rope  
        prior_strength (float): prior strength (default: 1)
        prior_place (LEFT, ROPE or RIGHT): the region to which the prior is
            assigned (default: ROPE)
        nsamples (int): the number of Monte Carlo samples
    
    Returns:
        2-d array with rows corresponding to samples and columns to
        probabilities `[p_left, p_rope, p_right]`
    """
    if prior_strength < 0:
        raise ValueError('Prior strength must be nonegative')
    if nsamples < 0:
        raise ValueError('Number of samples must be a positive integer')
    if rope < 0:
        raise ValueError('Rope must be a positive number')
    if x.ndim == 2:
        x = x[:, 1] - x[:, 0]
    nleft = sum(x < -rope)
    nright = sum(x > rope)
    nrope = len(x) - nleft - nright
    alpha = np.array([nleft, nrope, nright], dtype=float)
    alpha += 0.0001
    alpha[prior_place] += prior_strength
    return np.random.dirichlet(alpha, nsamples)


def signtest(x, rope, prior_strength=1, prior_place=ROPE, nsamples=50000, verbose=False, names=('C1', 'C2')):
    """
    Args:
        x (array): a vector of differences or a 2d array with pairs of scores.
        rope (float): the width of the rope  
        prior_strength (float): prior strength (default: 1)
        prior_place (LEFT, ROPE or RIGHT): the region to which the prior is
            assigned (default: ROPE)
        nsamples (int): the number of Monte Carlo samples
        verbose (bool): report the computed probabilities
        names (pair of str): the names of the two classifiers

    Returns:
        p_left, p_rope, p_right 
    """
    samples = signtest_MC(x, rope, prior_strength, prior_place, nsamples)
    winners = np.argmax(samples, axis=1)
    pl, pe, pr = np.bincount(winners, minlength=3) / len(winners)
    if verbose:
        print('P({c1} > {c2}) = {pl}, P(rope) = {pe}, P({c2} > {c1}) = {pr}'.format(c1=(names[0]),
          c2=(names[1]),
          pl=pl,
          pe=pe,
          pr=pr))
    return (
     pl, pe, pr)


def heaviside(X):
    Y = np.zeros(X.shape)
    Y[np.where(X > 0)] = 1
    Y[np.where(X == 0)] = 0.5
    return Y


def signrank_MC(x, rope, prior_strength=0.6, prior_place=ROPE, nsamples=50000):
    """
    Args:
        x (array): a vector of differences or a 2d array with pairs of scores.
        rope (float): the width of the rope  
        prior_strength (float): prior strength (default: 0.6)
        prior_place (LEFT, ROPE or RIGHT): the region to which the prior is
            assigned (default: ROPE)
        nsamples (int): the number of Monte Carlo samples
    
    Returns:
        2-d array with rows corresponding to samples and columns to
        probabilities `[p_left, p_rope, p_right]`
    """
    if x.ndim == 2:
        zm = x[:, 1] - x[:, 0]
    nm = len(zm)
    if prior_place == ROPE:
        z0 = [
         0]
    if prior_place == LEFT:
        z0 = [
         -float('inf')]
    if prior_place == RIGHT:
        z0 = [
         float('inf')]
    z = np.concatenate((zm, z0))
    n = len(z)
    z = np.transpose(np.asmatrix(z))
    X = np.matlib.repmat(z, 1, n)
    Y = np.matlib.repmat(-np.transpose(z) + 2 * rope, n, 1)
    Aright = heaviside(X - Y)
    X = np.matlib.repmat(-z, 1, n)
    Y = np.matlib.repmat(np.transpose(z) + 2 * rope, n, 1)
    Aleft = heaviside(X - Y)
    alpha = np.concatenate((np.ones(nm), [prior_strength]), axis=0)
    samples = np.zeros((nsamples, 3), dtype=float)
    for i in range(0, nsamples):
        data = np.random.dirichlet(alpha, 1)
        samples[(i, 2)] = numpy.inner(np.dot(data, Aright), data)
        samples[(i, 0)] = numpy.inner(np.dot(data, Aleft), data)
        samples[(i, 1)] = 1 - samples[(i, 0)] - samples[(i, 2)]

    return samples


def signrank(x, rope, prior_strength=0.6, prior_place=ROPE, nsamples=50000, verbose=False, names=('C1', 'C2')):
    """
    Args:
        x (array): a vector of differences or a 2d array with pairs of scores.
        rope (float): the width of the rope 
        prior_strength (float): prior strength (default: 0.6)
        prior_place (LEFT, ROPE or RIGHT): the region to which the prior is
            assigned (default: ROPE)
        nsamples (int): the number of Monte Carlo samples
        verbose (bool): report the computed probabilities
        names (pair of str): the names of the two classifiers

    Returns:
        p_left, p_rope, p_right
    """
    samples = signrank_MC(x, rope, prior_strength, prior_place, nsamples)
    winners = np.argmax(samples, axis=1)
    pl, pe, pr = np.bincount(winners, minlength=3) / len(winners)
    if verbose:
        print('P({c1} > {c2}) = {pl}, P(rope) = {pe}, P({c2} > {c1}) = {pr}'.format(c1=(names[0]),
          c2=(names[1]),
          pl=pl,
          pe=pe,
          pr=pr))
    return (
     pl, pe, pr)


def hierarchical(diff, rope, rho, upperAlpha=2, lowerAlpha=1, lowerBeta=0.01, upperBeta=0.1, std_upper_bound=1000, verbose=False, names=('C1', 'C2')):
    samples = hierarchical_MC(diff, rope, rho, upperAlpha, lowerAlpha, lowerBeta, upperBeta, std_upper_bound, names)
    winners = np.argmax(samples, axis=1)
    pl, pe, pr = np.bincount(winners, minlength=3) / len(winners)
    if verbose:
        print('P({c1} > {c2}) = {pl}, P(rope) = {pe}, P({c2} > {c1}) = {pr}'.format(c1=(names[0]),
          c2=(names[1]),
          pl=pl,
          pe=pe,
          pr=pr))
    return (
     pl, pe, pr)


def hierarchical_MC(diff, rope, rho, upperAlpha=2, lowerAlpha=1, lowerBeta=0.01, upperBeta=0.1, std_upper_bound=1000, names=('C1', 'C2')):
    import scipy.stats as stats
    import pystan
    stdX = np.mean(np.std(diff, 1))
    x = diff / stdX
    rope = rope / stdX
    for i in range(0, len(x)):
        if np.std(x[i, :]) == 0:
            x[i, :] = x[i, :] + np.random.normal(0, np.min(1e-09, np.abs(np.mean(x[i, :]) / 100000000)))

    hierarchical_code = "\n    /*Hierarchical Bayesian model for the analysis of competing cross-validated classifiers on multiple data sets.\n    */\n\n      data {\n\n        real deltaLow;\n        real deltaHi;\n\n        //bounds of the sigma of the higher-level distribution\n        real std0Low; \n        real std0Hi; \n\n        //bounds on the domain of the sigma of each data set\n        real stdLow; \n        real stdHi; \n\n\n        //number of results for each data set. Typically 100 (10 runs of 10-folds cv)\n        int<lower=2> Nsamples; \n\n        //number of data sets. \n        int<lower=1> q; \n\n        //difference of accuracy between the two classifier, on each fold of each data set.\n        matrix[q,Nsamples] x;\n\n        //correlation (1/(number of folds))\n        real rho; \n\n        real upperAlpha;\n        real lowerAlpha;\n        real upperBeta;\n        real lowerBeta;\n\n         }\n\n\n      transformed data {\n\n        //vector of 1s appearing in the likelihood \n        vector[Nsamples] H;\n\n        //vector of 0s: the mean of the mvn noise \n        vector[Nsamples] zeroMeanVec;\n\n        /* M is the correlation matrix of the mvn noise.\n        invM is its inverse, detM its determinant */\n        matrix[Nsamples,Nsamples] invM;\n        real detM;\n\n        //The determinant of M is analytically known\n        detM <- (1+(Nsamples-1)*rho)*(1-rho)^(Nsamples-1);\n\n        //build H and invM. They do not depend on the data.\n        for (j in 1:Nsamples){\n          zeroMeanVec[j]<-0;\n          H[j]<-1;\n          for (i in 1:Nsamples){\n            if (j==i)\n              invM[j,i]<- (1 + (Nsamples-2)*rho)*pow((1-rho),Nsamples-2);\n            else\n              invM[j,i]<- -rho * pow((1-rho),Nsamples-2);\n           }\n        }\n        /*at this point invM contains the adjugate of M.\n        we  divide it by det(M) to obtain the inverse of M.*/\n        invM <-invM/detM;\n      }\n\n      parameters {\n        //mean of the  hyperprior from which we sample the delta_i\n        real<lower=deltaLow,upper=deltaHi> delta0; \n\n        //std of the hyperprior from which we sample the delta_i\n        real<lower=std0Low,upper=std0Hi> std0;\n\n        //delta_i of each data set: vector of lenght q.\n        vector[q] delta;               \n\n        //sigma of each data set: : vector of lenght q.\n        vector<lower=stdLow,upper=stdHi>[q] sigma; \n\n        /* the domain of (nu - 1) starts from 0\n        and can be given a gamma prior*/\n        real<lower=0> nuMinusOne; \n\n        //parameters of the Gamma prior on nuMinusOne\n        real<lower=lowerAlpha,upper=upperAlpha> gammaAlpha;\n        real<lower=lowerBeta, upper=upperBeta> gammaBeta;\n\n      }\n\n     transformed parameters {\n        //degrees of freedom\n        real<lower=1> nu ;\n\n        /*difference between the data (x matrix) and \n        the vector of the q means.*/\n        matrix[q,Nsamples] diff; \n\n        vector[q] diagQuad;\n\n        /*vector of length q: \n        1 over the variance of each data set*/\n        vector[q] oneOverSigma2; \n\n        vector[q] logDetSigma;\n\n        vector[q] logLik;\n\n        //degrees of freedom\n        nu <- nuMinusOne + 1 ;\n\n        //1 over the variance of each data set\n        oneOverSigma2 <- rep_vector(1, q) ./ sigma;\n        oneOverSigma2 <- oneOverSigma2 ./ sigma;\n\n        /*the data (x) minus a matrix done as follows:\n        the delta vector (of lenght q) pasted side by side Nsamples times*/\n        diff <- x - rep_matrix(delta,Nsamples); \n\n        //efficient matrix computation of the likelihood.\n        diagQuad <- diagonal (quad_form (invM,diff'));\n        logDetSigma <- 2*Nsamples*log(sigma) + log(detM) ;\n        logLik <- -0.5 * logDetSigma - 0.5*Nsamples*log(6.283);  \n        logLik <- logLik - 0.5 * oneOverSigma2 .* diagQuad;\n\n      }\n\n      model {\n        /*mu0 and std0 are not explicitly sampled here.\n        Stan automatically samples them: mu0 as uniform and std0 as\n        uniform over its domain (std0Low,std0Hi).*/\n\n        //sampling the degrees of freedom\n        nuMinusOne ~ gamma ( gammaAlpha, gammaBeta);\n\n        //vectorial sampling of the delta_i of each data set\n        delta ~ student_t(nu, delta0, std0);\n\n        //logLik is computed in the previous block \n        increment_log_prob(sum(logLik));   \n     }\n    "
    datatable = x
    std_within = np.mean(np.std(datatable, 1))
    Nsamples = len(datatable[0])
    q = len(datatable)
    if q > 1:
        std_among = np.std(np.mean(datatable, 1))
    else:
        std_among = np.mean(np.std(datatable, 1))
    hierachical_dat = {'x':datatable, 
     'deltaLow':-np.max(np.abs(datatable)), 
     'deltaHi':np.max(np.abs(datatable)), 
     'stdLow':0, 
     'stdHi':std_within * std_upper_bound, 
     'std0Low':0, 
     'std0Hi':std_among * std_upper_bound, 
     'Nsamples':Nsamples, 
     'q':q, 
     'rho':rho, 
     'upperAlpha':upperAlpha, 
     'lowerAlpha':lowerAlpha, 
     'upperBeta':upperBeta, 
     'lowerBeta':lowerBeta}
    fit = pystan.stan(model_code=hierarchical_code, data=hierachical_dat, iter=1000,
      chains=4)
    la = fit.extract(permuted=True)
    mu = la['delta0']
    stdh = la['std0']
    nu = la['nu']
    samples = np.zeros((len(mu), 3), dtype=float)
    for i in range(0, len(mu)):
        samples[(i, 2)] = 1 - stats.t.cdf(rope, nu[i], mu[i], stdh[i])
        samples[(i, 0)] = stats.t.cdf(-rope, nu[i], mu[i], stdh[i])
        samples[(i, 1)] = 1 - samples[(i, 0)] - samples[(i, 2)]

    return samples


def plot_posterior(samples, names=('C1', 'C2'), proba_triplet=None):
    """
    Args:
        x (array): a vector of differences or a 2d array with pairs of scores.
        names (pair of str): the names of the two classifiers

    Returns:
        matplotlib.pyplot.figure
    """
    return plot_simplex(samples, names, proba_triplet)


def plot_simplex(points, names=('C1', 'C2'), proba_triplet=None):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.pylab import rcParams

    def _project(points):
        from math import sqrt, sin, cos, pi
        p1, p2, p3 = points.T / sqrt(3)
        x = (p2 - p1) * cos(pi / 6) + 0.5
        y = p3 - (p1 + p2) * sin(pi / 6) + 1 / (2 * sqrt(3))
        return np.vstack((x, y)).T

    vert0 = _project(np.array([
     [
      0.3333, 0.3333, 0.3333], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]]))
    fig = plt.figure()
    fig.set_size_inches(8, 7)
    nl, ne, nr = np.max(points, axis=0)
    for i, n in enumerate((nl, ne, nr)):
        if n < 0.001:
            print('p{} is too small, switching to 2d plot'.format(names[::-1] + ['rope']))
            coords = sorted(set(range(3)) - i)
            return plot2d(points[:, coords], labels[coords])

    fig.gca().add_line(Line2D([0, 0.5, 1.0, 0], [
     0, np.sqrt(3) / 2, 0, 0],
      color='black'))
    for i in (1, 2, 3):
        fig.gca().add_line(Line2D([vert0[(0, 0)], vert0[(i, 0)]], [
         vert0[(0, 1)], vert0[(i, 1)]],
          color='black'))

    rcParams.update({'font.size': 16})
    fig.gca().text((-0.08), (-0.08), ('p({} ({}))'.format(names[0], proba_triplet[0])), color='black')
    fig.gca().text(0.44, (np.sqrt(3) / 2 + 0.05), 'p(rope)', color='black')
    fig.gca().text(0.65, (-0.08), ('p({} ({}))'.format(names[1], proba_triplet[2])), color='black')
    tripts = _project(points[:, [0, 2, 1]])
    plt.hexbin((tripts[:, 0]), (tripts[:, 1]), mincnt=1, cmap=(plt.cm.Greens_r))
    fig.gca().set_xlim(-0.2, 1.2)
    fig.gca().set_ylim(-0.2, 1.2)
    fig.gca().axis('off')
    return fig