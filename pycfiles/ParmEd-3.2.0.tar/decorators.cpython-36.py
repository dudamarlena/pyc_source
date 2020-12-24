# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/decorators.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 1114 bytes
""" A list of helpful decorators for use throughout ParmEd """
__all__ = [
 'needs_openmm']
from parmed.utils.six import wraps
try:
    import simtk.openmm as mm, simtk.openmm.app as app
    HAS_OPENMM = True
    try:
        from simtk.openmm.app.internal import unitcell
    except ImportError:
        unitcell = None
        SUPPORTED_VERSION = False
    else:
        SUPPORTED_VERSION = True
except ImportError:
    HAS_OPENMM = False
else:
    del mm
    del app
    del unitcell
import warnings

def needs_openmm(fcn):

    @wraps(fcn)
    def new_fcn(*args, **kwargs):
        global HAS_OPENMM
        if not HAS_OPENMM:
            raise ImportError('Could not find or import OpenMM')
        if not SUPPORTED_VERSION:
            raise ImportError('You must have at least OpenMM 6.3 installed')
        return fcn(*args, **kwargs)

    return new_fcn


def deprecated(fcn):

    @wraps(fcn)
    def new_fcn(*args, **kwargs):
        warnings.warn('%s is deprecated and will be removed in the future' % fcn.__name__, DeprecationWarning)
        return fcn(*args, **kwargs)

    return new_fcn