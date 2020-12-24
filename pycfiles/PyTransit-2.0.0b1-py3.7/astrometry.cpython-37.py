# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/astrometry.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 1487 bytes
from orbits.orbits_py import a_from_mp
from .constants import msun, mjup
as_c = {'as':1.0, 
 'mas':1000.0,  'muas':1000000.0}

def angular_signal(mass, period, distance, mstar=1.0, units='as'):
    """Angular semi-amplitude of the astrometric signal caused by a planet.
    
    Parameters
    ----------

      mass     : planet mass            [M_Jup]
      period   : orbital period         [d]
      distance : distance to the system [pc]
      mstar    : stellar mass           [M_Sun]
      units    : 'as', 'mas', or 'muas'

    Returns
    -------

      angular semi-amplitude of the astrometric signal by the planet in given units

    """
    return as_c[units] * (mass * mjup) / (mstar * msun) * a_from_mp(mstar, period) / distance