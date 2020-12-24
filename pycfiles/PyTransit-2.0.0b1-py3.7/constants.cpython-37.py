# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/constants.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 2652 bytes
"""Astrophysical quantities

 Astrophysical quantities with their error estimates
 ===================================================

 Notes
 -----
  Error estimates follow the form Q_e where Q is the
  quantity in question, and are available only for a
  subset of quantities.

 =============  ============================== ======
 ``au``         astronomical unit                   m
 ``msun``       solar mass                         kg
 ``rsun``       solar radius                        m
 ``dsun``       mean solar mass density        g/cm^3
 ``mjup``       Jupiter mass                       kg
 ``rjup``       volumetric mean Jupiter radius      m
 ``rjup_eq``    equatorial Jupiter radius           m
 ``djup``       mean Jupiter mass density      g/cm^3
 ``mnep``       Neptune mass            radius     kg
 ``rnep``       volumetric mean Neptune radius      m
 ``rnep_eq``    equatorial Neptune radius           m
 ``djup``       mean Neptune mass density      g/cm^3
 ``rearth``     volumetric mean Earth radius        m
 ``rearth_eq``  equatorial Earth radius             m
 =============  ============================== ======
"""
from __future__ import division
d_h = 24.0
d_m = 60 * d_h
d_s = 60 * d_m
au, au_e = (149600000000.0, 0.0)
msun, msun_e = (1.9891e+30, 0.0)
rsun, rsun_e = (696342000.0, 0.0)
dsun, dsun_e = (1.408, 0.0)
mjup, mjup_e = (1.89896e+27, 0.0)
rjup, rjup_e = (69911000.0, 0.0)
rjup_eq, rjup_eq_e = (71492000.0, 0.0)
djup, djup_e = (1.326, 0.0)
mnep, mnep_e = (1.0242e+26, 0.0)
rnep, mnep_e = (24622000.0, 0.0)
rnep_eq, mnep_eq_e = (24764000.0, 0.0)
dnep, dnep_e = (1.638, 0.0)
mearth, mearth_e = (5.9726e+24, 0.0)
rearth, rearth_e = (6371000.0, 0.0)
rearth_eq, rearth_eq_e = (6378100.0, 0.0)
dearth, dearth_e = (5.514, 0.0)