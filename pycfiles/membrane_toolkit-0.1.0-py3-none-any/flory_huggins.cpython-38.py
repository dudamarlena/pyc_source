# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/core/flory_huggins.py
# Compiled at: 2020-05-10 20:17:24
# Size of source mod 2**32: 724 bytes
"""
Placeholder for code implementing the Flory-Huggins model of solvent
activity inside membranes.
"""

def flory_huggins_chi():
    """
    Calculate the Flory-Huggins chi parameter from water uptake.

# Calculate the Flory-Huggins interaction parameter by assuming that the water sorption data fit Flory-Huggins theory
#
# $$ \\chi = \x0crac{\\ln{\x0crac{a_w}{\\phi_w} }-1+\\phi_w}{(1-\\phi_w)^2} $$

    def calculate_chi(row):
    chi = (math.log(row['Water Activity']/row['Vol_frac'])-1+row['Vol_frac'])/(1 - row['Vol_frac'])**2
    return chi

    """
    pass