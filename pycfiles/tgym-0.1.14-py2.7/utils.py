# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tgym/utils.py
# Compiled at: 2017-06-15 04:42:39


def calc_spread(prices, spread_coefficients):
    """Calculate the spread based on spread_coefficients.

    Args:
        spread_coefficients (list): A list of signed integers defining how much
            of each product to buy (positive) or sell (negative) when buying or
            selling the spread.
        prices (numpy.array): Array containing the prices (bid, ask) of
            different products, i.e: [p1_b, p1_a, p2_b, p2_a].

    Returns:
        tuple:
            - (float) spread bid price,
            - (float) spread ask price.
    """
    spread_bid = sum([ spread_coefficients[i] * prices[(2 * i + int(spread_coefficients[i] < 0))] for i in range(len(spread_coefficients))
                     ])
    spread_ask = sum([ spread_coefficients[i] * prices[(2 * i + int(spread_coefficients[i] > 0))] for i in range(len(spread_coefficients))
                     ])
    return (
     spread_bid, spread_ask)