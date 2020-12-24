# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\ctf\colortf.py
# Compiled at: 2018-05-03 00:00:22
# Size of source mod 2**32: 4779 bytes
"""
###################################################
 Extension of basic colorimetry module
###################################################
 
Global internal variables:
    
 :_COLORTF_DEFAULT_WHITE_POINT: ndarray with XYZ values of default white point 
                                (equi-energy white) for color transformation 
                                if none is supplied.

Functions:

 :colortf(): Calculates conversion between any two color spaces ('cspace')
              for which functions xyz_to_cspace() and cspace_to_xyz() are defined.

===============================================================================
"""
from luxpy import *
__all__ = [
 '_COLORTF_DEFAULT_WHITE_POINT', 'colortf']
_COLORTF_DEFAULT_WHITE_POINT = np.array([100.0, 100.0, 100.0])

def colortf(data, tf=_CSPACE, fwtf={}, bwtf={}, **kwargs):
    """
    Wrapper function to perform various color transformations.
    
    Args:
        :data: 
            | ndarray
        :tf: 
            | _CSPACE or str specifying transform type, optional
            |     E.g. tf = 'spd>xyz' or 'spd>Yuv' or 'Yuv>cct' 
            |      or 'Yuv' or 'Yxy' or ...
            |  If tf is for example 'Yuv', it is assumed to be a transformation 
               of type: 'xyz>Yuv'
        :fwtf: 
            | dict with parameters (keys) and values required 
              by some color transformations for the forward transform: 
            | i.e. 'xyz>...'
        :bwtf:
            | dict with parameters (keys) and values required 
              by some color transformations for the backward transform: 
            | i.e. '...>xyz'

    Returns:
        :returns: 
            | ndarray with data transformed to new color space
        
    Note:
        For the forward transform ('xyz>...'), one can input the keyword 
        arguments specifying the transform parameters directly without having 
        to use the dict :fwtf: (should be empty!) 
        [i.e. kwargs overwrites empty fwtf dict]
    """
    tf = tf.split('>')
    if len(tf) == 1:
        if not bool(fwtf):
            fwtf = kwargs
        return (globals()['{}_to_{}'.format('xyz', tf[0])])(data, **fwtf)
    if not bool(fwtf):
        fwtf = kwargs
    bwfcn = globals()['{}_to_{}'.format(tf[0], 'xyz')]
    fwfcn = globals()['{}_to_{}'.format('xyz', tf[1])]
    return fwfcn(bwfcn(data, **bwtf), **fwtf)