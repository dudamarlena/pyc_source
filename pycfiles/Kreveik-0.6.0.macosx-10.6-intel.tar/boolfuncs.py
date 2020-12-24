# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/network/boolfuncs/boolfuncs.py
# Compiled at: 2012-09-09 23:45:49
"""

"""
import numpy as num, logging, boolfuncs_c

def xor_masking(network, state):
    """
   
    """
    state = num.array(state, dtype=bool)
    newstate = num.array([None] * network.n_nodes)
    for i in xrange(network.n_nodes):
        nonzero_of_adj = network.adjacency[(i,)].nonzero()[0]
        short_mask = network.mask[(i,)].take(nonzero_of_adj)
        short_state = state.take(nonzero_of_adj)
        newstate[i] = num.logical_xor(short_mask, short_state).sum() < len(short_state) / 2.0

    try:
        return newstate
    except:
        logging.error('XOR masking failed in network')
        logging.error('Printing id:')
        logging.error(id(network))
        return False

    return


def and_masking(network, state):
    """

    """
    state = num.array(state)
    newstate = num.zeros(network.n_nodes)
    for i in range(0, network.n_nodes):
        nonzero_of_adj = network.adjacency[(i,)].nonzero()[0]
        short_mask = network.mask[(i,)].take(nonzero_of_adj)
        short_state = state.take(nonzero_of_adj)
        sum_of_bool = num.logical_and(short_mask, short_state).sum()
        newstate[i] = len(short_state) / 2.0 < sum_of_bool

    try:
        return newstate
    except:
        logging.error('AND masking failed in network')
        logging.error('Printing id:')
        logging.error(id(network))
        return False


def or_masking(network, state):
    """

    """
    newstate = num.zeros(network.n_nodes)
    for i in range(0, network.n_nodes):
        nonzero_of_adj = network.adjacency[(i,)].nonzero()[0]
        short_mask = network.mask[(i,)].take(nonzero_of_adj)
        short_state = network.state[(-1)].take(nonzero_of_adj)
        sum_of_bool = num.logical_or(short_mask, short_state).sum()
        newstate[i] = len(short_state) / 2.0 < sum_of_bool

    try:
        return newstate
    except:
        logging.error('OR masking failed in network')
        logging.error('Printing id:')
        logging.error(id(network))
        return False


def xor_masking_C(network, state):
    newstate = boolfuncs_c.xor_masking_c(network.adjacency, network.mask, state)
    return newstate


def or_masking_C(network, state):
    newstate = boolfuncs_c.or_masking_c(network.adjacency, network.mask, state)
    return newstate


def and_masking_C(network, state):
    newstate = boolfuncs_c.and_masking_c(network.adjacency, network.mask, state)
    return newstate