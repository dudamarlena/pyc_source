# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/siddon/models.py
# Compiled at: 2011-02-08 06:07:56
"""
Defines various tomography models and priors to be used with an optimizer.

- srt : Solar rotational tomography (with priors)
- stsrt : Smooth temporal rotational tomography
- thomson : Thomson scattering model
"""
import numpy as np, copy, lo, siddon
from lo_wrapper import siddon_lo, siddon4d_lo
import solar
sigma = 1.0

def srt(data, cube, **kwargs):
    """
    Define Solar Rotational Tomography model with optional masking of
    data and map areas. Can also define priors.
    
    Parameters
    ----------
    data: InfoArray
        data cube
    cube: FitsArray
        map cube
    obj_rmin: float
        Object minimal radius. Areas below obj_rmin are masked out.
    obj_rmax: float
        Object maximal radius. Areas above obj_rmax are masked out.
    data_rmin: float
        Data minimal radius. Areas below data_rmin are masked out.
    data_rmax: float
        Data maximal radius. Areas above data_rmax are masked out.
    mask_negative: boolean
        If true, negative values in the data are masked out.

    Returns
    -------
    P : The projector with masking
    D : Smoothness priors
    obj_mask : object mask array
    data_mask : data mask array

    """
    data_mask = solar.define_data_mask(data, **kwargs)
    P = siddon_lo(data.header, cube.header, mask=data_mask, obstacle='sun')
    D = [ lo.diff(cube.shape, axis=i) for i in xrange(cube.ndim) ]
    P, D, obj_mask = _apply_object_mask(P, D, cube, **kwargs)
    return (P, D, obj_mask, data_mask)


def _apply_object_mask(P, D, cube, **kwargs):
    obj_rmin = kwargs.get('obj_rmin', None)
    obj_rmax = kwargs.get('obj_rmax', None)
    if obj_rmin is not None or obj_rmax is not None:
        Mo, obj_mask = mask_object(cube, **kwargs)
        P = P * Mo.T
        D = [ Di * Mo.T for Di in D ]
    else:
        obj_mask = None
    return (
     P, D, obj_mask)


def _apply_data_mask(P, data, **kwargs):
    data_rmin = kwargs.get('data_rmin', None)
    data_rmax = kwargs.get('data_rmax', None)
    mask_negative = kwargs.get('mask_negative', False)
    mask_nan = kwargs.get('mask_nan', True)
    if data_rmin is not None or data_rmax is not None or mask_negative is not False or mask_nan is not False:
        data_mask = solar.define_data_mask(data, **kwargs)
        Md = lo.mask(data_mask)
        P = Md * P
    else:
        data_mask = None
    return (
     P, data_mask)


def stsrt(data, cube, **kwargs):
    """
    Smooth Temporal Solar Rotational Tomography.
    Assumes data is sorted by observation time 'DATE_OBS'.

    Returns
    -------
    P : The projector with masking
    D : Smoothness priors
    obj_mask : object mask array
    data_mask : data mask array
    """
    obj_rmin = kwargs.get('obj_rmin', None)
    obj_rmax = kwargs.get('obj_rmax', None)
    data_mask = solar.define_data_mask(data, **kwargs)
    times = [ solar.convert_time(h['DATE_OBS']) for h in data.header ]
    dt_min = kwargs.get('dt_min', np.max(np.diff(times)) + 1)
    ind = solar.temporal_groups_indexes(data, dt_min)
    n = len(ind)
    cube4 = cube[(..., np.newaxis)].repeat(n, axis=-1)
    cube4.header = copy.copy(cube.header)
    cube4.header['NAXIS'] = 4
    cube4.header['NAXIS4'] = cube4.shape[3]
    ng = data.shape[(-1)] / n
    P = siddon4d_lo(data.header, cube4.header, ng=ng, mask=data_mask, obstacle='sun')
    D = [ lo.diff(cube4.shape, axis=i) for i in xrange(cube4.ndim) ]
    if obj_rmin is not None or obj_rmax is not None:
        Mo, obj_mask = mask_object(cube, **kwargs)
        obj_mask = obj_mask[(..., np.newaxis)].repeat(n, axis=-1)
        Mo = lo.mask(obj_mask)
        P = P * Mo.T
        D = [ Di * Mo.T for Di in D ]
    else:
        obj_mask = None
    return (
     P, D, obj_mask, data_mask)


def mask_object(cube, decimate=False, remove_nan=False, **kwargs):
    obj_rmin = kwargs.get('obj_rmin', None)
    obj_rmax = kwargs.get('obj_rmax', None)
    if obj_rmin is not None or obj_rmax is not None:
        obj_mask = solar.define_map_mask(cube, **kwargs)
        if decimate:
            Mo = lo.decimate(obj_mask, dtype=cube.dtype)
        else:
            Mo = lo.mask(obj_mask, dtype=cube.dtype, remove_nan=remove_nan)
    return (
     Mo, obj_mask)


def group_sum(ind, cube, data):
    from lo import ndsubclass
    shapein = cube.shape + (data.shape[(-1)],)
    shapeout = cube.shape + (len(ind),)
    ind1 = ind
    ind2 = ind1[1:] + [None]
    axis = -1

    def matvec(x):
        out = np.zeros(shapeout)
        for i, j, k in zip(ind1, ind2, np.arange(len(ind1))):
            out[(..., k)] = x[..., i:j].sum(axis=-1)

        return out

    def rmatvec(x):
        out = np.zeros(shapein)
        for i, j, k in zip(ind1, ind2, np.arange(len(ind1))):
            tmp_shape = out[..., i:j].shape
            out[..., i:j] = x[(..., k)].repeat(tmp_shape[(-1)]).reshape(tmp_shape)

        return out

    return lo.ndoperator(shapein, shapeout, matvec, rmatvec, dtype=np.float64)


def thomson(data, cube, u=0.5, **kwargs):
    """
    Defines a Thomson scattering model for white light coronographs.

    Parameters
    ----------
    data: 3D InfoArray
      Data stack.
    cube: 3D FitsArray
      Map cube.

    Returns
    -------
    P : The projector with masking
    D : Smoothness priors
    obj_mask : object mask array
    data_mask : data mask array
    """
    data_mask = solar.define_data_mask(data, **kwargs)
    pb = kwargs.get('pb', 'pb')
    if pb == 'pb':
        P = pb_thomson_lo(data, cube, u, mask=data_mask)
    else:
        raise ValueError('Only pb implemented for now.')
    D = [ lo.diff(cube.shape, axis=i) for i in xrange(cube.ndim) ]
    P, D, obj_mask = _apply_object_mask(P, D, cube, remove_nan=True, **kwargs)
    return (P, D, obj_mask, data_mask)


def pb_thomson_lo(data, in_map, u, mask=None):
    """Defines thomson scattering linear operator"""
    data_coefs = _pb_data_coef(data).flatten()
    O = lo.diag(data_coefs)
    map_coefs = _pb_map_coef(in_map, u).flatten()
    M = lo.diag(map_coefs)
    P = siddon_lo(data.header, in_map.header, obstacle='sun', mask=mask)
    T = O * P * M
    return T


def _r2omega(r):
    """Compute the Omega angle knowing r (see Bilings 66 for def)."""
    omega = np.zeros(r.shape)
    omega = np.arcsin(1.0 / r)
    omega[r == 0] = 0
    return omega


def _impact_parameter(alpha, beta, d):
    """Impact parameter of a line. Set to 1. if < 1. """
    from numpy import sin, cos, arccos
    rho = d * sin(arccos(cos(alpha) * cos(beta)))
    rho[rho < 1.0] = 1.0
    return rho


def _thomson_coef(omega):
    """Thomson scattering coefficients as defined by Billings."""
    sino = np.sin(omega)
    sino2 = sino ** 2
    coso = np.cos(omega)
    coso2 = coso ** 2
    lno = np.log((1.0 + sino) / coso) * (coso2 / sino)
    C1 = coso * sino2
    C2 = -(1.0 / 8.0) * (1.0 - 3.0 * sino2 - (1.0 + 3.0 * sino2) * lno)
    C3 = 4.0 / 3.0 - coso * (1.0 + coso2 / 3.0)
    C4 = 1.0 / 8.0 * (5.0 + sino2 - (5.0 - sino2) * lno)
    return (C1, C2, C3, C4)


def _pb_thomson_coef(omega):
    """Thomson scattering coefficients as defined by Billings.
    Computes only the first 2 required for pB model.
    """
    sino = np.sin(omega)
    sino2 = sino ** 2
    coso = np.cos(omega)
    coso2 = coso ** 2
    lno = np.log((1.0 + sino) / coso) * (coso2 / sino)
    C1 = coso * sino2
    C2 = -(1.0 / 8.0) * (1.0 - 3.0 * sino2 - (1.0 + 3.0 * sino2) * lno)
    return (C1, C2)


def _pb_data_coef(data):
    """Returns pb coefficients for a data array."""
    from fitsarray import asfitsarray
    coefs = np.zeros(data.shape)
    for i in xrange(data.shape[(-1)]):
        im = asfitsarray(solar.slice_data(data, i))
        alpha, beta = im.axes()
        Alpha, Beta = np.meshgrid(alpha, beta)
        coefs[(..., i)] = _impact_parameter(Alpha, Beta, im.header['D']) ** 2

    return coefs


def _pb_map_coef(my_map, u):
    """Returns pb map coefficients corresponding to a map array."""
    from fitsarray import asfitsarray
    coefs = np.zeros(my_map.shape)
    x, y, z = asfitsarray(my_map).axes()
    x2 = x ** 2
    y2 = y ** 2
    z2 = z ** 2
    X2, Y2 = np.meshgrid(x2, y2)
    for i, z2i in enumerate(z2):
        R2 = X2 + Y2 + z2i
        R = np.sqrt(R2)
        O = _r2omega(R)
        C1, C2 = _pb_thomson_coef(O)
        coefs[(..., i)] = ((1 - u) * C1 + u * C2) / R2

    coefs[1 - np.isfinite(coefs)] = 0.0
    return coefs * np.pi * sigma / 2.0