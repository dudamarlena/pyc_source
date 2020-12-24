# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/State.py
# Compiled at: 2019-01-04 14:13:16
# Size of source mod 2**32: 2382 bytes
""" Computes acceleration and ionization on a packet due to specified forces

Gravitational acceleration

Equations of motion:
    dvxdt = sum_objects (GM * (x-x_obj))/(r_obj)^3
    dvydt = sum_objects (GM * (y-y_obj))/(r_obj)^3
    dvzdt = sum_objects (GM * (z-z_obj))/(r_obj)^3
        -- r_obj = sqrt( (x-x_obj)^2 + (y-y_obj)^2 + (z-z_obj)^2 )
    dndt = instantaneous change in density

Current version: Assumes there is only a planet -- does not do moons yet
"""
import numpy as np
from astropy.time import Time

def State(t, x, v, output):
    if output.inputs.forces.gravity:
        r3 = (x[0, :] ** 2 + x[1, :] ** 2 + x[2, :] ** 2) ** 1.5
        agrav = output.GM * x / r3
    else:
        agrav = np.zeros_like(x)
    arad = np.zeros_like(x)
    if output.inputs.forces.radpres:
        rho = x[0, :] ** 2 + x[2, :] ** 2
        out_of_shadow = (rho > 1) | (x[1, :] < 0)
        vv = v[1, :] + output.vrplanet
        arad[1, :] = np.interp(vv, output.radpres.velocity, output.radpres.accel) * out_of_shadow
    else:
        accel = agrav + arad
        if not np.all(np.isfinite(accel)):
            raise AssertionError
        elif output.inputs.options.lifetime > 0:
            ionizerate = np.ones_like(t) / output.inputs.options.lifetime.value
        else:
            if output.loss_info.photo is not None:
                rho = x[0, :] ** 2 + x[2, :] ** 2
                out_of_shadow = (rho > 1) | (x[1, :] < 0)
                photorate = output.loss_info.photo * out_of_shadow
            else:
                photorate = 0.0
        ionizerate = photorate
        return (
         accel, ionizerate)