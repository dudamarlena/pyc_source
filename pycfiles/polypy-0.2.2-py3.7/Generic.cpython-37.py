# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polypy/Generic.py
# Compiled at: 2018-12-06 12:38:59
# Size of source mod 2**32: 1849 bytes
import os, sys, numpy as np
import matplotlib.pyplot as plt
from polypy import Read as rd
from polypy import Density as Dens
from polypy import Utils as Ut
from polypy import Write as wr
from scipy import stats
from scipy.constants import codata

def pbc(rnew, rold, vec):
    """
    pbc - Periodic boundary conditions for an msd calculation
    Parameters
    ----------
    rnew  : Value of current atomic position   : Float
    rold  : Value of previous atomic position  : Float
    vec   : Lattice vector at that timestep    : Float
    
    Return
    ------
    cross  : Result of PBC check - True if atom crosses the boundary   : Bool
    new    : New position                                              : Float
    """
    shift = abs((rold - rnew) / vec)
    shift = round(shift, 0)
    shift = int(shift)
    cross = False
    if shift < 2:
        if rnew - rold > vec * 0.5:
            rnew = rnew - vec
            cross = True
        elif -(rnew - rold) > vec * 0.5:
            rnew = rnew + vec
            cross = True
    elif rnew - rold > vec * 0.5:
        rnew = rnew - vec * shift
        cross = True
    else:
        if -(rnew - rold) > vec * 0.5:
            rnew = rnew + vec * shift
            cross = True
    return (
     cross, rnew)


def bin_choose(X, Y):
    """
    BinChoose - Calculate the number of bins depending on a box size and a bin thickness
    Parameters
    ----------
    X  : box length    : Float
    Y  : bin thickness : Float
             
    Return
    ------
    Z  : Number of bins : Float
    """
    Z = X / Y
    Z = round(Z, 0)
    Z = int(Z)
    Z = Z - 1
    return Z


def get_integer(x, y):
    z = x / y
    z = round(z, 0)
    z = int(z)
    return z