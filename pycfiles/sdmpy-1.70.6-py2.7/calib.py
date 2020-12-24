# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/calib.py
# Compiled at: 2020-01-07 17:38:36
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import numpy as np
from numpy import linalg
try:
    import casatools
except ImportError:
    casatools = None

from .bdf import ant2bl, bl2ant

def gaincal(data, axis=0, ref=0, avg=[], nit=3):
    """Derives amplitude/phase calibration factors from the data array
    for the given baseline axis.  In the returned array, the baseline
    dimension is converted to antenna.  No other axes are modified.
    Note this internally makes a transposed copy of the data so be
    careful with memory usage in the case of large data sets.  A list
    of axes to average over before solving can be given in the avg
    argument (length-1 dimensions are kept so that the solution can be
    applied to the original data)."""
    nbl = data.shape[axis]
    ndim = len(data.shape)
    check, nant = bl2ant(nbl)
    if check != 0:
        raise RuntimeError(b'Specified axis dimension (%d) is not a valid number of baselines' % nbl)
    for a in avg:
        data = data.mean(axis=a, keepdims=True)

    tdata = np.zeros(data.shape[:axis] + data.shape[axis + 1:] + (nant, nant), dtype=data.dtype)
    for i in range(nbl):
        a0, a1 = bl2ant(i)
        tdata[(..., a0, a1)] = data.take(i, axis=axis)
        tdata[(..., a1, a0)] = np.conj(data.take(i, axis=axis))

    for it in range(nit):
        wtmp, vtmp = linalg.eigh(tdata)
        v = vtmp[(Ellipsis, -1)].copy()
        w = wtmp[(Ellipsis, -1)]
        for i in range(nant):
            tdata[(..., i, i)] = w * (v.real[(..., i)] ** 2 + v.imag[(..., i)] ** 2)

    result = np.sqrt(w).T * v.T
    result = (result * np.conj(result[ref]) / np.abs(result[ref])).T
    outdims = list(range(axis)) + [-1] + list(range(axis, ndim - 1))
    return result.transpose(outdims)


def applycal(data, caldata, axis=0, phaseonly=False):
    """
    Apply the complex gain calibration given in the caldata array
    to the data array.  The baseline/antenna axis must be specified in
    the axis argument.  Dimensions of all other axes must match up
    (in the numpy broadcast sense) between the two arrays.
    """
    ndim = len(data.shape)
    nbl = data.shape[axis]
    nant = caldata.shape[axis]
    check, nant_check = bl2ant(nbl)
    if check != 0:
        raise RuntimeError(b'Specified axis dimension (%d) is not a valid number of baselines' % nbl)
    if nant != nant_check:
        raise RuntimeError(b'Number of antennas does not match (data=%d, caldata=%d)' % (nant_check, nant))
    if phaseonly:
        caldata = caldata.copy() / abs(caldata)
        caldata[np.where(np.isfinite(caldata) is False)] = complex(0.0, 0.0)
    for ibl in range(nbl):
        dslice = (
         slice(None),) * axis + (ibl,) + (slice(None),) * (ndim - axis - 1)
        a1, a2 = bl2ant(ibl)
        calfac = 1.0 / (caldata.take(a1, axis=axis) * caldata.take(a2, axis=axis).conj())
        calfac[np.where(np.isfinite(calfac) is False)] = complex(0.0, 0.0)
        data[dslice] *= calfac

    return


def hanning(data, axis=0):
    """Apply hanning smoothing along the specified axis, typically this should
    be the spectral channel axis.  Modifies data array in-place."""
    data_pos = np.roll(data, 1, axis=axis)
    data_neg = np.roll(data, -1, axis=axis)
    data += 0.5 * (data_pos + data_neg)
    data *= 0.5


def uvw(mjd, direction, antpos):
    """Return an Nbaseline-x-3 array giving U,V,W in meters for
    the given MJD, sky direction, and antenna positions.

      direction is (ra,dec) in radians
      antpos is Nant-by-3 array of antenna positions in meters.

    This can be called on an sdmpy Scan object like:

      uvw = sdmpy.calib.uvw(scan.startMJD, scan.coordinates, scan.positions)
    """
    if casatools is None:
        raise RuntimeError(b'')
    me = casatools.measures()
    qa = casatools.quanta()
    qq = qa.quantity
    s = me.direction(b'J2000', qq(direction[0], b'rad'), qq(direction[1], b'rad'))
    e = me.epoch(b'UTC', qq(mjd, b'd'))
    o = me.observatory(b'VLA')
    me.doframe(o)
    me.doframe(e)
    me.doframe(s)
    pos = np.array(antpos)
    casapos = me.position(b'ITRF', qq(pos[:, 0], b'm'), qq(pos[:, 1], b'm'), qq(pos[:, 2], b'm'))
    bls = me.expand(me.touvw(me.asbaseline(casapos))[0])[1][b'value']
    bls = bls.reshape((-1, 3))
    nant = pos.shape[0]
    nbl = bls.shape[0]
    oidx = [ ant2bl((i, j)) for i in range(nant) for j in range(i + 1, nant) ]
    uvw = 0.0 * bls
    for i in range(nbl):
        uvw[oidx[i], :] = bls[i, :]

    return uvw