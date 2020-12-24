# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyabm\statistics.py
# Compiled at: 2013-02-01 18:05:57
"""
Contains miscellaneous functions useful in running statistics for agent-based models.
"""
from pyabm import np

class UnitsError(Exception):
    pass


class StatisticsError(Exception):
    pass


def convert_probability_units(probability, prob_time_units):
    """
    Converts probability so units match timestep used in the model, assuming probability 
    function is uniform across the interval.

    Conversions are made accordingly using conditional probability.
    """
    if prob_time_units == 'months':
        pass
    elif prob_time_units == 'years':
        for key, value in probability.items():
            probability[key] = 1 - (1 - value) ** (1 / 12.0)

    elif prob_time_units == 'decades':
        for key, value in probability.items():
            probability[key] = 1 - (1 - value) ** (1 / 120.0)

    else:
        raise UnitsError('unhandled prob_time_units')
    return probability


def get_probability_index(t, prob_time_units):
    """
    Matches units of time in model to those the probability is expressed in. For 
    instance: if probabilities are specified for decades, whereas the model runs in 
    months, ``get_probability_index``, when provided with an age in months, will convert 
    it to decades, rounding down. NOTE: all probabilities must be expressed with the 
    same time units.
    """
    if prob_time_units == 'months':
        return t
    if prob_time_units == 'years':
        return int(round(t / 12.0))
    if prob_time_units == 'decades':
        return int(round(t / 120.0))
    raise UnitsError('unhandled prob_time_units')


def draw_from_prob_dist(prob_dist):
    """
    Draws a random number from a manually specified probability distribution,
    where the probability distribution is a tuple specified as::

        ([a, b, c, d], [1, 2, 3])

    where a, b, c, and d are bin limits, and 1, 2, and 3 are the probabilities 
    assigned to each bin. Notice one more bin limit must be specified than the 
    number of probabilities given (to close the interval).
    """
    binlims, probs = prob_dist
    num = np.random.rand() * np.sum(probs)
    n = 0
    probcumsums = np.cumsum(probs)
    for problim in probcumsums[0:-1]:
        if num < problim:
            break
        n += 1

    upbinlim = binlims[(n + 1)]
    lowbinlim = binlims[n]
    return np.random.uniform(lowbinlim, upbinlim)


def calc_prob_from_prob_dist(prob_dist, attribute):
    """
    Calculates the probability of something based on a manually specified 
    probability distribution, where the probability distribution is a tuple 
    specified as::

        ([a, b, c, d], [1, 2, 3])

    where a, b, c, and d are bin limits, and 1, 2, and 3 are the probabilities 
    assigned to each bin. Notice one more bin limit must be specified than the 
    number of probabilities given (to close the interval). The bin limits are 
    closed on the right, open on the left.

    The correct probability to draw is based on the bin that the 'attribute' 
    parameter falls into. For example, to draw the probability of marrying a 
    spouse based on the difference in age between the spouse and a particular 
    agent, 'attribute' should be the age difference. This function will then 
    return the probability of marrying that spouse based on the bin that the 
    spouse age difference falls into.
    """
    binlims, probs = prob_dist
    n = 0
    for uplim in binlims[1:]:
        if attribute <= uplim:
            break
        n += 1

    return probs[n]


def calc_coefficient(coef_tuple):
    """
    Use to handle uncertainty in regression coefficients. ``calc_coefficient`` 
    takes in a tuple of two floats::

        (coef, stderror)

    where coef is the estimated regression coefficient, and stderror is the 
    standard error of the estimated coefficient.
    """
    if len(coef_tuple) != 2:
        raise ValueError('coef_tuple must be of the from (coef, stderror)')
    return coef_tuple[0] + np.random.randn() * coef_tuple[1]