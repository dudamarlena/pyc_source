# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\spectrum\basics\cmf.py
# Compiled at: 2020-02-06 14:58:04
# Size of source mod 2**32: 7075 bytes
"""
Module for Color Matching Functions (CMF) and Vlambda (=Ybar)
=============================================================

cmf.py
------

  :luxpy._CMF: | Dict with keys 'types' and x
               | x are dicts with keys 'bar', 'K', 'M'
 
     | * luxpy._CMF['types']  = ['1931_2','1964_10','2006_2','2006_10',
                                 '1931_2_judd1951','1931_2_juddvos1978',
                                 '1951_20_scotopic']
     | * luxpy._CMF[x]['bar'] = numpy array with CMFs for type x 
                                between 360 nm and 830 nm (has shape: (4,471))
     | * luxpy._CMF[x]['K']   = Constant converting Watt to lumen for CMF type x.
     | * luxpy._CMF[x]['M']   = XYZ to LMS conversion matrix for CMF type x.
                                Matrix is numpy array with shape: (3,3)
                            
     Notes:
         
        1. All functions have been expanded (when necessary) using zeros to a 
            full 360-830 range. This way those wavelengths do not contribute 
            in the calculation, AND are not extrapolated using the closest 
            known value, as per CIE recommendation.

        2. There are no XYZ to LMS conversion matrices defined for the 
            1964 10°, 1931 2° Judd corrected (1951) 
            and 1931 2° Judd-Vos corrected (1978) cmf sets.
            The Hunt-Pointer-Estevez conversion matrix of the 1931 2° is 
            therefore used as an approximation!
            
        3. The K lm to Watt conversion factors for the Judd and Judd-Vos cmf 
            sets have been set to 683.002 lm/W (same as for standard 1931 2°).
            
        4. The 1951 scoptopic V' function has been replicated in the 3 
            xbar, ybar, zbar columns to obtain a data format similar to the 
            photopic color matching functions. 
            This way V' can be called in exactly the same way as other V 
            functions can be called from the X,Y,Z cmf sets. 
            The K value has been set to 1700.06 lm/W and the conversion matrix 
            to np.eye().
        
        5. _CMF[x]['M'] for x equal to '2006_2' or '2006_10' is NOT 
            normalized to illuminant E! These are the original matrices 
            as defined by [1] & [2].

    
References
----------

    1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_

    2. `CIE, and CIE (2006). 
    Fundamental Chromaticity Diagram with Physiological Axes - Part I.(Vienna: CIE).
    <http://www.cie.co.at/publications/fundamental-chromaticity-diagram-physiological-axes-part-1>`_

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, math
__all__ = [
 '_CMF']
_CMF_TYPES = [
 '1931_2', '1964_10', '2006_2', '2006_10', '1931_2_judd1951', '1931_2_juddvos1978', '1951_20_scotopic', 'cie_std_dev_obs_f1']
_CMF_K_VALUES = [683.002, 683.599, 683.358, 683.144, 683.002, 683.002, 1700.06, 0.0]
_CMF_M_1931_2 = np.array([
 [
  0.38971, 0.68898, -0.07868],
 [
  -0.22981, 1.1834, 0.04641],
 [
  0.0, 0.0, 1.0]])
_CMF_M_2006_2 = np.linalg.inv(np.array([[1.94735469, -1.41445123, 0.36476327],
 [
  0.68990272, 0.34832189, 0],
 [
  0, 0, 1.93485343]]))
_CMF_M_2006_10 = np.linalg.inv(np.array([[1.93986443, -1.34664359, 0.43044935],
 [
  0.69283932, 0.34967567, 0],
 [
  0, 0, 2.14687945]]))
_CMF_M_1964_10 = np.array([
 [
  0.38971, 0.68898, -0.07868],
 [
  -0.22981, 1.1834, 0.04641],
 [
  0.0, 0.0, 1.0]])
_CMF_M_1931_2_JUDD1951 = np.array([
 [
  0.38971, 0.68898, -0.07868],
 [
  -0.22981, 1.1834, 0.04641],
 [
  0.0, 0.0, 1.0]])
_CMF_M_1931_2_JUDDVOS1978 = np.array([
 [
  0.38971, 0.68898, -0.07868],
 [
  -0.22981, 1.1834, 0.04641],
 [
  0.0, 0.0, 1.0]])
_CMF_M_1951_20_SCOTOPIC = np.eye(3)
_CMF_M_cie_std_dev_obs_f1 = np.eye(3)
_CMF_M_list = [
 _CMF_M_1931_2, _CMF_M_1964_10, _CMF_M_2006_2, _CMF_M_2006_10, _CMF_M_1931_2_JUDD1951, _CMF_M_1931_2_JUDDVOS1978, _CMF_M_1951_20_SCOTOPIC, _CMF_M_cie_std_dev_obs_f1]
_CMF = {'types': _CMF_TYPES}
for i, cmf_type in enumerate(_CMF_TYPES):
    _CMF[cmf_type] = {'bar': []}
    _CMF[cmf_type]['K'] = _CMF_K_VALUES[i]
    _CMF[cmf_type]['M'] = _CMF_M_list[i]