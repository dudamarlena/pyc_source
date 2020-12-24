# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/network/scorers.py
# Compiled at: 2012-09-09 23:45:49
"""
scorers module
===============

This module contains different scorer functions that have a 
single network as input and outputs its score accordingly.

Functions
---------
    sum_scorer_f:
    orbit_length_sum_f
 
"""

def sum_scorer_f(network):
    """
    This function takes a network object and returns its score 
    computed by summing the lengths of orbits for every single 
    possible initial condition. If initial conditions turn 
    out to have the same attractors, they are counted again.
    """
    network.populate_equilibria()
    return sum(network.equilibria) / 2.0 ** network.n_nodes


def orbit_length_sum_f(network):
    """
    This function takes a network object and and returns its 
    score computed by summing the lengths of genuine orbits.
    """
    import numpy as num
    binspace = range(0, num.power(2, network.n_nodes))
    genuine_orbits = []
    genuine_orbit_lengths = []
    for state in binspace:
        orbit_length, orbit = network.search_equilibrium(2 ** network.n_nodes, state, True)
        is_in_list = False
        for old_orbit in genuine_orbits:
            for state in old_orbit:
                if all(state == orbit[(-1)]):
                    is_in_list = True

        if is_in_list == False:
            genuine_orbits.append(orbit)
            genuine_orbit_lengths.append(orbit_length)

    return sum(genuine_orbit_lengths)