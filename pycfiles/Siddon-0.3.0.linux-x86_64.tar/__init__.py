# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/siddon/__init__.py
# Compiled at: 2011-02-08 10:15:57
"""
This packages implements tomography algorithms and utilities in
python. It is made of several modules

- siddon: The core of the package, with a fast C/OpenMP
  implementation of the Siddon algorithm.
  See : http://adsabs.harvard.edu/abs/1985MedPh..12..252S

- simu: Implements some utilities to perform simulations.

- solar: A module to load Solar physics data with appropriate
  metadata.

- phantom: To generate phantoms (Shepp-Logan, Modified Shepp Logan,
  and Yu Ye Wang phantoms).

"""
from siddon import *
import simu, solar, phantom, models
try:
    import lo
except ImportError:
    pass

if 'lo' in locals():
    from lo_wrapper import *
version = '0.3.0'