# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lib.py
# Compiled at: 2014-11-26 17:37:26
import numpy as np
ROMSVARS = dict(his=dict(axes=['ocean_time',
 's_rho',
 'eta_rho',
 'xi_rho'], variables=[
 'zeta',
 'ubar_eastward',
 'vbar_northward',
 'u_eastward',
 'v_northward',
 'temp',
 'salt']), rst=dict(axes=['ocean_time',
 's_rho',
 'eta_rho',
 'xi_rho',
 'eta_u',
 'xi_u',
 'eta_v',
 'xi_v'], variables=[
 'zeta',
 'ubar',
 'vbar',
 'u',
 'v',
 'temp',
 'salt']), clim=dict(axes=['ocean_time',
 's_rho',
 'eta_rho',
 'xi_rho',
 'eta_u',
 'xi_u',
 'eta_v',
 'xi_v'], variables=[
 'zeta',
 'ubar',
 'vbar',
 'u',
 'v',
 'temp',
 'salt']))

class RomsGrid(object):
    """ 
    Stores and manipulates netcdf ROMS grid file information
    """

    def __init__(self, filename):
        self.filename = filename
        self.ncfile = nc.Dataset(filename, mode='r+')
        self.lonr = self.ncfile.variables['lon_rho'][:]
        self.latr = self.ncfile.variables['lat_rho'][:]
        self.lonu = self.ncfile.variables['lon_u'][:]
        self.latu = self.ncfile.variables['lat_u'][:]
        self.lonv = self.ncfile.variables['lon_v'][:]
        self.latv = self.ncfile.variables['lat_v'][:]
        self.h = self.ncfile.variables['h'][:]
        self.maskr = self.ncfile.variables['mask_rho'][:]
        self.masku = self.ncfile.variables['mask_u'][:]
        self.maskv = self.ncfile.variables['mask_v'][:]


def near2d(x, y, x0, y0):
    """
    Find the indexes of the grid point that is
    nearest a chosen (x0, y0).
    Usage: line, col = near2d(x, y, x0, y0)
    """
    dx = np.abs(x - x0)
    dx = dx / dx.max()
    dy = np.abs(y - y0)
    dy = dy / dy.max()
    dn = dx + dy
    fn = np.where(dn == dn.min())
    line = int(fn[0])
    col = int(fn[1])
    return (line, col)


def get_zlev(h, sigma, hc, sc, ssh=0.0, Vtransform=2):
    if Vtransform == 1:
        hinv = 1.0 / h
        cff = hc * (sc - sigma)
        if len(h.shape) > 1:
            z0 = cff[:, None, None] + sigma[:, None, None] * h[None, :, :]
        else:
            z0 = cff[:, None] + sigma[:, None] * h[None, :]
        return z0 + ssh * (1.0 + z0 * hinv)
    else:
        if Vtransform == 2:
            if len(h.shape) > 1:
                z0 = (hc * sc[:, None, None] + sigma[:, None, None] * h[None, :, :]) / (h[None, :, :] + hc)
            else:
                z0 = (hc * sc[:, None] + sigma[:, None] * h[None, :]) / (h[None, :] + hc)
            return ssh + (ssh + h) * z0
        return