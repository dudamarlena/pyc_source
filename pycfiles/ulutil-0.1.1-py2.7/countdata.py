# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/countdata.py
# Compiled at: 2014-12-19 21:46:23
"""
countdata.py

Functions for stats and analysis of count data.

"""
import sys, numpy as np, scipy as sp

def sample2counts(sample, categories=0):
    """Return count vector from list of samples.
    
    Take vector of samples and return a vector of counts.  The elts
       refer to indices in something that would ultimately map to the
       originating category (like from a multinomial).  Therefore, if there
       are, say, 8 categories, then valid values in sample should be 0-7.
       If categories is not given, then i compute it from the highest value
       present in sample (+1).
    
    """
    counts = np.bincount(sample)
    if categories > 0 and categories > len(counts):
        counts = np.append(counts, np.zeros(categories - len(counts)))
    return counts


def counts2sample(counts):
    """Computes a consistent sample from a vector of counts.
    
    Takes a vector of counts and returns a vector of indices x
       such that len(x) = sum(c) and each elt of x is the index of
       a corresponding elt in c
    
    """
    x = np.ones(np.sum(counts), dtype=np.int_)
    start_idx = 0
    end_idx = 0
    for i in xrange(len(counts)):
        start_idx = end_idx
        end_idx = end_idx + counts[i]
        x[start_idx:end_idx] = x[start_idx:end_idx] * i

    return x


def scoreatpercentile(values, rank):
    return sp.stats.scoreatpercentile(values, rank)


def percentileofscore(values, score):
    values.sort()
    return values.searchsorted(score) / np.float_(len(values))


def qvalues(p, lambd=np.arange(0, 0.91, 0.05), method='bootstrap', B=100, smoothlog=False, robust=False):
    """Compute q-values using Storey method from array of p-values.
    
    Adapted from his R software.
    
    """
    p = np.array(p)
    if np.min(p) < 0 or np.max(p) > 1:
        raise Exception, 'p-values not in valid range'
    m = len(p)
    pi0 = np.zeros(len(lambd))
    for i in np.arange(len(lambd)):
        pi0[i] = np.mean(p >= lambd[i]) / (1 - lambd[i])

    if method == 'bootstrap':
        minpi0 = np.min(pi0)
        mse = np.zeros(len(lambd))
        pi0_boot = np.zeros(len(lambd))
        for i in np.arange(B):
            p_boot = p[np.random.randint(0, m, m)]
            for j in np.arange(len(lambd)):
                pi0_boot[j] = np.mean(p_boot >= lambd[j]) / (1 - lambd[j])

            mse += (pi0_boot - minpi0) ** 2

        pi0 = np.min(pi0[(mse == np.min(mse))])
        pi0 = np.min(pi0, 1)
    elif method == 'smoother':
        print 'Not implemented yet'
        return
    if pi0 <= 0:
        raise Exception, 'The estimated pi0 <=0.  May be problem with pvalues.'
    u = np.argsort(p)
    v = qvalrank(p)
    qvalue = pi0 * m * p / v
    if robust == True:
        qvalue = pi0 * m * p / (v * (1 - (1 - p) ** m))
    qvalue[u[(m - 1)]] = np.min([qvalue[u[(m - 1)]], 1])
    for i in np.arange(m - 2, -1, -1):
        qvalue[u[i]] = np.min([qvalue[u[i]], qvalue[u[(i + 1)]], 1])

    return qvalue


def qvalrank(x):
    idx = np.argsort(x)
    levels = np.unique(x)
    bin = levels.searchsorted(x)
    tbl = np.bincount(bin)
    cs = np.cumsum(tbl)
    tbl = cs.repeat(tbl)
    tbl2 = np.zeros(len(tbl), np.int_)
    tbl2[idx] = tbl
    return tbl2


def pval_KalZtest(n1, N1, n2, N2):
    """Compute p-value using Kal Z-test for count data.
    
    Compute pval using Z-test, as published in
    Kal et al, 1999, Mol Biol Cell 10:1859.
    
    Z = (p1-p2) / sqrt( p0 * (1-p0) * (1/N1 + 1/N2) )
    where p1 = n1/N1, p2=n2/N2, and p0=(n1+n2)/(N1+N2)
    You reject if |Z| > Z_a/2 where a is sig lev.  Here
    we return the p-value itself.
    
    """
    if n1 == 0 and n2 == 0:
        return 1.0
    n1 = np.float_(n1)
    N1 = np.float_(N1)
    n2 = np.float_(n2)
    N2 = np.float_(N2)
    p0 = (n1 + n2) / (N1 + N2)
    p1 = n1 / N1
    p2 = n2 / N2
    Z = (p1 - p2) / np.sqrt(p0 * (1 - p0) * (1 / N1 + 1 / N2))
    pval = 2 * sp.stats.norm.cdf(-1 * abs(Z))
    return pval


def pval_KalZtest_vec(n1, N1, n2, N2):
    assert n1.shape[0] == n2.shape[0]
    p0 = (n1 + n2) / (float(N1) + N2)
    p1 = n1 / float(N1)
    p2 = n2 / float(N2)
    p0[(n1 == 0) & (n2 == 0)] = 0.5
    Z = (p1 - p2) / np.sqrt(p0 * (1.0 - p0) * (1.0 / N1 + 1.0 / N2))
    pval = 2 * sp.stats.norm.cdf(-1 * abs(Z))
    pval[(n1 == 0) & (n2 == 0)] = -1.0
    return pval


def pval_logRatioMC(n1, N1, n2, N2):
    pass


def pvals_logRatioMC(counts1, counts2, B=1000000.0, pseudocount=1, verbose=False):
    """Compute component-wise p-values of difference between two count vectors
    using Monte Carlo sampling of log ratios.
    
    Null hypothesis is that data is from same multinomial.  Parameters estimated
    by combining both count vectors.  Zeros are handled by adding pseudocount to
    each element.
    
    The test statistic is log Ratio, which is computed for each component.
    
    Two random count vectors are generated, and and component-wise log ratio
    is computed.  For each component, it is recorded whether the abs random log
    ratio was greater than or less than the abs test statistic value.  This is
    performed B times.  The absolute value makes the test two-sided and symmetric.
    
    The achieved significance level (ASL) is returned for each component.
    
    """
    if len(counts1) != len(counts2):
        raise ValueError, 'Counts vectors have different lengths.'
    counts1 = np.asarray(counts1, dtype=np.float)
    counts2 = np.asarray(counts2, dtype=np.float)
    total1 = int(np.round(np.sum(counts1)))
    total2 = int(np.round(np.sum(counts2)))
    countsMLE = counts1 + counts2 + pseudocount
    counts1 = counts1 + pseudocount
    counts2 = counts2 + pseudocount
    normcounts1 = counts1 / np.sum(counts1)
    normcounts2 = counts2 / np.sum(counts2)
    testabslogratios = np.abs(np.log10(normcounts2 / normcounts1))
    probvec = countsMLE / np.sum(countsMLE)
    atleastasextreme = np.zeros(len(counts1))
    for i in xrange(B):
        if verbose and i % 10 == 0:
            sys.stdout.write('%i ' % i)
            sys.stdout.flush()
        randcounts1 = np.float_(np.random.multinomial(total1, probvec)) + pseudocount
        randcounts2 = np.float_(np.random.multinomial(total2, probvec)) + pseudocount
        normrandcounts1 = randcounts1 / np.sum(randcounts1)
        normrandcounts2 = randcounts2 / np.sum(randcounts2)
        randabslogratios = np.abs(np.log10(normrandcounts2 / normrandcounts1))
        atleastasextreme += np.float_(randabslogratios >= testabslogratios)

    ASL = atleastasextreme / B
    return ASL


def pvals_counts(counts1, counts2, method='KalZtest'):
    """Compute component-wise p-values of difference between two count vectors.
    
    method can be one of:
        KalZtest
        MonteCarlo
    
    """
    if len(counts1) != len(counts2):
        raise ValueError, 'Counts vectors have different lengths.'
    pvals = np.zeros(len(counts1))
    N1 = np.sum(counts1)
    N2 = np.sum(counts2)
    if method == 'KalZtest':
        for i in xrange(len(pvals)):
            pvals[i] = pval_KalZtest(counts1[i], N1, counts2[i], N2)

    elif method == 'MonteCarlo':
        pvals = pvals_logRatioMC(counts1, counts2, B=1000000.0, pseudocounts=1)
    else:
        raise Exception, method + ' is not a recognized method for computing p-values.'
    return pvals


def gen_rand_count_vec(numComponents, numCounts, fracNull, probvecNull, probvecAlt):
    pass