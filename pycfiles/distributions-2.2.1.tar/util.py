# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: distributions/util.py
# Compiled at: 2017-10-28 18:53:45
import numpy

def scores_to_probs(scores):
    scores = numpy.array(scores)
    scores -= scores.max()
    probs = numpy.exp(scores, out=scores)
    probs /= probs.sum()
    return probs


def score_to_empirical_kl(score, count):
    """
    Convert total log score to KL( empirical || model ),
    where the empirical pdf is uniform over `count` datapoints.
    """
    count = float(count)
    return -score / count - numpy.log(count)


def bin_samples(samples, k=10, support=[]):
    """
    Bins a collection of univariate samples into k bins of equal
    fill via the empirical cdf, to be used in goodness of fit testing.

    Returns
    counts : array k x 1
    bin_ranges : arrary k x 2

    each count is the number of samples in [bin_min, bin_max)
    except for the last bin which is [bin_min, bin_max]

    list partitioning algorithm adapted from Mark Dickinson:
    http://stackoverflow.com/questions/2659900
    """
    samples = sorted(samples)
    N = len(samples)
    q, r = divmod(N, k)
    indices = [ i * q + min(r, i) for i in range(k + 1) ]
    bins = [ samples[indices[i]:indices[(i + 1)]] for i in range(k) ]
    bin_ranges = []
    counts = []
    for i in range(k):
        bin_min = bins[i][0]
        try:
            bin_max = bins[(i + 1)][0]
        except IndexError:
            bin_max = bins[i][(-1)]

        bin_ranges.append([bin_min, bin_max])
        counts.append(len(bins[i]))

    if support:
        bin_ranges[0][0] = support[0]
        bin_ranges[(-1)][1] = support[1]
    return (
     numpy.array(counts), numpy.array(bin_ranges))


def histogram(samples, bin_count=None):
    if bin_count is None:
        bin_count = numpy.max(samples) + 1
    v = numpy.zeros(bin_count, dtype=int)
    for sample in samples:
        v[sample] += 1

    return v