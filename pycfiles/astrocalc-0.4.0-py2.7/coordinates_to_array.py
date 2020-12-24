# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/coords/coordinates_to_array.py
# Compiled at: 2020-05-01 12:03:38
"""
*Convert single values of RA, DEC or list of RA and DEC to numpy arrays*

:Author:
    David Young
"""
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import numpy as np
from astrocalc.coords import unit_conversion

def coordinates_to_array(log, ra, dec):
    """*Convert a single value RA, DEC or list of RA and DEC to numpy arrays*

    **Key Arguments**

    - ``ra`` -- list, numpy array or single ra value
    - ``dec`` --list, numpy array or single dec value
    - ``log`` -- logger
    

    **Return**

    - ``raArray`` -- input RAs as a numpy array of decimal degree values
    - ``decArray`` -- input DECs as a numpy array of decimal degree values
    

    **Usage**

    .. todo::

        add usage info
        create a sublime snippet for usage

    ```python
    ra, dec = coordinates_to_array(
        log=log,
        ra=ra,
        dec=dec
    )
    ```
    
    """
    log.debug('starting the ``coordinates_to_array`` function')
    if isinstance(ra, np.ndarray) and isinstance(dec, np.ndarray):
        return (ra, dec)
    converter = unit_conversion(log=log)
    if isinstance(ra, float):
        pass
    elif isinstance(ra, (('').__class__, ('').__class__)):
        try:
            ra = float(ra)
        except:
            ra = converter.ra_sexegesimal_to_decimal(ra=ra)

    elif isinstance(ra, list):
        try:
            ra = np.array(ra).astype(np.float)
        except:
            raList = []
            raList[:] = [ converter.ra_sexegesimal_to_decimal(ra=r) for r in ra ]
            ra = raList

    if isinstance(dec, float):
        pass
    elif isinstance(dec, (('').__class__, ('').__class__)):
        try:
            dec = float(dec)
        except:
            dec = converter.dec_sexegesimal_to_decimal(dec=dec)

    elif isinstance(dec, list):
        try:
            dec = np.array(dec).astype(np.float)
        except:
            decList = []
            decList[:] = [ converter.dec_sexegesimal_to_decimal(dec=d) for d in dec ]
            dec = decList

    raArray = np.array(ra, dtype='f8', ndmin=1, copy=False)
    decArray = np.array(dec, dtype='f8', ndmin=1, copy=False)
    log.debug('completed the ``coordinates_to_array`` function')
    return (raArray, decArray)