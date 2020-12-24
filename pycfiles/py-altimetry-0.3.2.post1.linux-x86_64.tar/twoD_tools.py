# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/twoD_tools.py
# Compiled at: 2016-03-23 12:35:00
"""
Created on 30 janv. 2013

@author: rdussurg
"""
import numpy as np
from altimetry.tools import interp1d, calcul_distance, deriv, gravity, coriolis
import matplotlib.pyplot as plt

def uvgrid(*args, **kwargs):
    lon = args[0]
    lat = args[1]
    if len(args) == 3:
        sla = args[2]
        time = np.arange(1)
    else:
        time = args[2]
        sla = args[3]
    strict = kwargs.get('strict', False)
    nx = len(lon)
    ny = len(lat)
    nt = len(time)
    sla = sla.reshape((nt, ny, nx))
    nxout = nx - 1 if strict else nx
    nyout = ny - 1 if strict else ny
    dx = np.median(deriv(lon))
    dy = np.median(deriv(lat))
    xgrad = np.repeat([ calcul_distance(l, 0.0, l, dx) * 1000.0 for l in np.float64(lat) ], nx).reshape((ny, nx))
    ygrad = np.repeat(calcul_distance(0, 0, dy, 0) * 1000.0, nx * ny).reshape((ny, nx))
    lonout = interp1d(np.arange(nx), lon, np.arange(nxout) + 0.5) if strict else lon
    latout = interp1d(np.arange(ny), lat, np.arange(nyout) + 0.5) if strict else lat
    glon, glat = np.meshgrid(lonout, latout)
    g = gravity(glat)
    f = coriolis(glat)
    dhx = np.ma.array(np.zeros((nt, nyout, nxout)), mask=True)
    dhx.data[:] = dhx.fill_value
    dhy = dhx.copy()
    dhdx = dhx.copy()
    dhdy = dhx.copy()
    u = dhx.copy()
    v = dhx.copy()
    for i in np.arange(nt):
        if strict:
            dhx[i, :, :] = np.diff(sla[i, :, :], axis=1)
            dhy[i, :, :] = np.diff(sla[i, :, :], axis=0)
        else:
            dhy[i, :, :], dhx[i, :, :] = np.gradient(sla[i, :, :])
        dhdx[i, :, :] = dhx[i, :, :] / xgrad
        dhdy[i, :, :] = dhy[i, :, :] / ygrad
        u[i, :, :] = -(g * dhdy[i, :, :]) / f
        v[i, :, :] = g * dhdx[i, :, :] / f

    u = np.squeeze(u)
    v = np.squeeze(v)
    return (
     u, v)