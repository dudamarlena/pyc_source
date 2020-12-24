# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/util/R_utilities.py
# Compiled at: 2013-04-04 09:39:31
"""
Created on Aug 8, 2010

@author: jonathanfriedman

TODO: make a general Rwrapper decorator 
"""
import numpy as np, rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.numpy2ri import numpy2ri
ro.conversion.py2ri = numpy2ri
from numpy import array

def fisher_test(counts):
    """
    Returns the 2 sided p-value from a fisher exact test.
    Counts is a np array representing the counts in the contingency table.
    Online doc: http://www.astrostatistics.psu.edu/datasets/R/html/stats/html/fisher.test.html
    """
    rstats = importr('stats')
    ans = rstats.fisher_test(counts)
    p_val = np.array(ans.rx2('p.value'))
    return p_val


def is_pd(mat):
    """
    Check if matrix is positive definite.
    Return bool
    Online doc: http://www.uni-leipzig.de/~strimmer/lab/software/corpcor/html/rank.condition.html
    """
    corpcor = importr('corpcor')
    flag = str(corpcor.is_positive_definite(mat)[0])
    if flag is 'False':
        return False
    else:
        return True


def make_pd(mat, package='matrix', corr=False, **kwargs):
    """
    computes the nearest positive definite of a real symmetric matrix, using the algorithm of NJ Higham (1988, Linear Algebra Appl. 103:103-118). 
    Online doc: http://www.uni-leipzig.de/~strimmer/lab/software/corpcor/html/rank.condition.html
                http://stat.ethz.ch/R-manual/R-devel/library/Matrix/html/nearPD.html
    """
    if package is 'corpcor':
        corpcor = importr('corpcor')
        mat_pd = np.array(corpcor.make_positive_definite(mat))
    elif package is 'matrix':
        Rmat = importr('Matrix')
        pd = np.array(Rmat.nearPD(mat, corr=corr))[0]
        x = np.array(pd.do_slot('x'))
        mat_pd = x.reshape(mat.shape)
    return mat_pd


def pcor(mat):
    """
    Compute the partial correlation matrix of data matrix.
    """
    corpcor = importr('corpcor')
    print corpcor.pcor_shrink(mat)


def var_shrink(data):
    """
    Estimate variance of data using James-Stein shrinkage toward the median variance (of all variables).
    In data, rows are observations and cols are variables.
    Online doc: http://strimmerlab.org/software/corpcor/html/cov.shrink.html
    """
    corpcor = importr('corpcor')
    var = np.array(corpcor.var_shrink(data))
    return var


def c_means(data, k, r=2, metric='euclidean', maxit=10000.0, diss=False):
    """
    Do fuzzy c-means clustering using R function 'fanny' from the 'cluster' library.
    Rows are observations (to be clusters), and cols are variables.
    k = number of clusters.
    r = fuzziness exponent. Less fuzzy as r -> 1.
    maxit = maximum number of iterations
        
    Online documentation: http://stat.ethz.ch/R-manual/R-devel/library/cluster/html/fanny.html
    """
    import scipy.cluster.hierarchy as sch
    rclust = importr('cluster')
    if diss:
        D = data
    else:
        D = sch.distance.pdist(data, metric=metric)
        D = sch.distance.squareform(D)
    ans = rclust.fanny(D, k, diss=True, memb_exp=r, maxit=maxit)
    membership = np.array(ans.rx2('membership'))
    membership_hard = np.array(ans.rx2('clustering'))
    coeff = np.array(ans.rx2('coeff'))
    k_crisp = np.array(ans.rx2('k.crisp'))
    silinfo = ans.rx2('silinfo')
    avg_width = np.array(silinfo.rx2('avg.width'))
    clust_avg_width = np.array(silinfo.rx2('clus.avg.widths'))
    stats = {'coeff': coeff, 'k_crisp': k_crisp, 'avg_width': avg_width, 'clust_avg_width': clust_avg_width}
    return (
     membership, membership_hard, stats)


def dirichlet_estimate(data):
    """
    Estimate the parameters of a dirichlet distribution from observed data.
    Inputs:
        data = [array] rows are realizations, cols are categories.
                       values are probability of category in given realization.
                       value must be in [0,1), and rows sum to 1.
    Online doc: http://rss.acs.unt.edu/Rdoc/library/VGAM/html/dirichlet.html
    """
    r = ro.r
    vgam = importr('VGAM')
    r.assign('y', data)
    fit = r('fit = vglm(y ~ 1, dirichlet, trace = FALSE, crit="c")')
    a = np.array(vgam.Coef(fit))
    ll = np.array(r.logLik(fit))
    return (a, ll)


def betbino_estimate(data):
    """
    Estimate the parameters of a beta-binomial distribution.
    Inputs:
    data = [array] rows are realizations, cols are categories (success and fail).
                   values are counts (or probability?) of category in given realization.
    """
    r = ro.r
    vgam = importr('VGAM')
    r.assign('y', data)
    fit = r('fit = vglm(y ~ 1, betabinomial, trace = FALSE)')
    a = np.array(vgam.Coef(fit))
    ll = np.array(r.logLik(fit))
    return (a, ll)


def pbetabin(k, N, a, b):
    """
    CDF of beta binomial.
    Online doc: http://rss.acs.unt.edu/Rdoc/library/VGAM/html/betabinUC.html
    """
    vgam = importr('VGAM')
    if isinstance(k, (int, float)):
        k = np.array([k])
    if isinstance(N, (int, float)):
        N = np.array([N])
    if not len(k) == len(N):
        raise ValueError, 'k and N must be of same length!'
    F = []
    for (ki, Ni) in zip(k, N):
        F += list(vgam.pbetabin_ab(ki, Ni, a, b))

    return np.array(F)


def dbetabin(k, N, a, b):
    """
    PMF of beta binomial.
    """
    vgam = importr('VGAM')
    if isinstance(k, (int, float)):
        k = np.array([k])
    if isinstance(N, (int, float)):
        N = np.array([N])
    if not len(k) == len(N):
        raise ValueError, 'k and N must be of same length!'
    F = []
    for (ki, Ni) in zip(k, N):
        F += list(vgam.dbetabin_ab(ki, Ni, a, b))

    return np.array(F)


def rbetabin(n, N, a, b):
    """
    rvs from betabinomial
    """
    vgam = importr('VGAM')
    rvs = vgam.rbetabin_ab(n, N, a, b)
    return np.array(rvs)


def dirmulti_estimate(data):
    """
    Estimate the parameters of a dirichlet-multinomial distribution.
    Inputs:
    data = [array] rows are realizations, cols are categories.
                   values are counts (or probability?) of category in given realization.
    
    Note that the parameterization of the distribution in this package is not the standard one.
    The parameters used are pi_i (i = 1:k-1) and phi, where pi_i is the expected value of x_i, and phi is the 'intracluster correlation'.
    Relation of fitted parameters to 'standard' dirichlet parameters:
    pi_i  = a_i/a0
    phi = 1/(a0+1)
    
    Online doc: http://rss.acs.unt.edu/Rdoc/library/VGAM/html/dirmultinomial.html
    """
    from numpy import exp
    r = ro.r
    vgam = importr('VGAM')
    r.assign('y', data)
    fit = r('fit = vglm(y ~ 1, dirmultinomial(parallel= TRUE, zero=NULL), trace = TRUE)')
    logit_phi = np.array(r('coef(fit)'))[(-1)]
    pi = np.array(vgam.fitted(fit))[0, :]
    phi = exp(logit_phi) / (1 + exp(logit_phi))
    a0 = (1 - phi) / phi
    a = pi * a0
    ll = np.array(r.logLik(fit))
    return (a, ll)


def multinomial_estimate(data):
    """
    Estimate the parameters of a multinomial distribution.
    Inputs:
    data = [array] rows are realizations, cols are categories.
                   values are counts (or probability?) of category in given realization.
    Online doc: http://rss.acs.unt.edu/Rdoc/library/VGAM/html/multinomial.html
    """
    r = ro.r
    vgam = importr('VGAM')
    r.assign('y', data)
    fit = r('fit = vglm(y ~ 1, multinomial, trace = FALSE)')
    a = np.array(vgam.fitted(fit))[0, :]
    ll = np.array(r.logLik(fit))
    return (a, ll)


def mvn_rv(mu, sigma, n):
    """
    Generate n samples from a multivariate normal with mean mu and covariance matrix sigma.
    """
    r_mvn = importr('mvtnorm')
    samples = r_mvn.rmvnorm(n, mu, sigma)
    return np.array(samples)


def logitnorm_pdf(x, mu, sigma):
    """
    Get the pdf of a logitnormal distribution with parameters mu & sigma, evaluated at points x.
    """
    r_logitnorm = importr('logitnorm')
    pdf = r_logitnorm.dlogitnorm(x, mu, sigma)
    return np.array(pdf)


def kder(x, adjust=1):
    """
    Kernel density estimation.
    Online doc: http://sekhon.berkeley.edu/stats/html/density.html
    """
    r_stat = importr('stats')
    kde = r_stat.density(x, adjust=adjust)
    points = np.array(kde.rx2('x'))
    pdf = np.array(kde.rx2('y'))
    return (points, pdf)


def qqplot(y, x, show=True):
    """
    Make a Quantile-Quantile plot of two datasets, or dataset against samples from theoretical distribution
    Online doc: http://sekhon.berkeley.edu/stats/html/qqnorm.html
    """
    import matplotlib.pyplot as plt
    r = ro.r
    r_stat = importr('stats')
    r.assign('x', x)
    r.assign('y', y)
    (qx, qy) = array(r('qqplot(y, x, plot.it = FALSE)'))
    if show:
        plt.figure()
        plt.plot(qx, qy, 'o')
        plt.plot(plt.xlim(), plt.xlim(), '--')
        plt.show()
    return (
     qx, qy)


def qqnorm(y, show=True):
    """
    Make a Quantile-Quantile plot of a data set against the best fitting normal distribution.
    Online doc: http://sekhon.berkeley.edu/stats/html/qqnorm.html
    """
    import matplotlib.pyplot as plt
    r = ro.r
    r_stat = importr('stats')
    r.assign('y', y)
    (qx, qy) = array(r('qqnorm(y, plot.it = FALSE)'))
    if show:
        plt.figure()
        plt.plot(qx, qy, 'o')
        plt.show()
    return (
     qx, qy)


def R_qvalues(p_vals):
    qlib = importr('qvalue')
    ans = qlib.qvalue(p_vals)
    q_vals = np.array(ans.rx2('qvalues'))
    return q_vals


def fdrtool(vals, **kwargs):
    fdrtool = importr('fdrtool')
    kwargs.setdefault('statistic', 'pvalue')
    kwargs.setdefault('plot', False)
    vals = np.asarray(vals)
    Rvals = ro.FloatVector(vals)
    ans = fdrtool.fdrtool(Rvals, **kwargs)
    qvals = np.array(ans.rx2('qval'))
    pvals = np.array(ans.rx2('pval'))
    return (
     pvals, qvals)


def entropy(x, method='shrink'):
    """
    Use the R entropy package to calculate the entropy of observations x using given method.
    Return the entropy value. 
    Valid methods: "ML", "MM", "Jeffreys", "Laplace", "SG", "minimax", "CS", "NSB", "shrink".
    Online Doc: http://strimmerlab.org/software/entropy/ 
    """
    rentropy = importr('entropy')
    H = np.array(rentropy.entropy(x, method=method))
    return H


if __name__ == '__main__':
    pass