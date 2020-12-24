# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/bouncepackets.py
# Compiled at: 2018-12-18 15:28:51
# Size of source mod 2**32: 2380 bytes
import numpy as np
from .input_classes import AngularDist
from .source_distribution import angular_distribution

def bouncepackets(self, t1, x1, v1, f1, hhh):
    x0 = x1[(0, hhh)]
    y0 = x1[(1, hhh)]
    z0 = x1[(2, hhh)]
    r0 = np.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2)
    vx0 = v1[(0, hhh)]
    vy0 = v1[(1, hhh)]
    vz0 = v1[(2, hhh)]
    a = vx0 ** 2 + vy0 ** 2 + vz0 ** 2
    b = 2 * (x0 * vx0 + y0 * vy0 + z0 * vz0)
    c = x0 ** 2 + y0 ** 2 + z0 ** 2 - 1.0
    dd = b ** 2 - 4 * a * c
    assert np.all(dd >= 0)
    t0 = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    t1 = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    t = (t0 <= 0) * t0 + (t1 < 0) * t1
    x2 = x0 + vx0 * t
    y2 = y0 + vy0 * t
    z2 = z0 + vz0 * t
    assert np.all(np.isfinite(x2))
    assert np.all(np.isfinite(y2))
    assert np.all(np.isfinite(z2))
    lonhit = (np.arctan2(x2, -y2) + 2 * np.pi) % (2 * np.pi)
    lathit = np.arcsin(z2)
    x1[(0, hhh)] = x2
    x1[(1, hhh)] = y2
    x1[(2, hhh)] = z2
    PE = 2 * self.GM * (1.0 / r0 - 1)
    vv02 = a + PE
    vv02[vv02 < 0] = 0.0
    assert np.all(np.isfinite(vv02))
    if self.inputs.sticking_info.emitfn.lower() == 'maxwellian':
        assert 0, 'Not set up yet'
        if self.inputs.sticking_info.Tsurf == 0:
            surftemp = SurfaceTemperatue(self.inputs.geometry, lonhit, lathit)
        else:
            pass
    else:
        if self.inputs.sticking_info.emitfn.lower() == 'elastic scattering':
            vv2 = np.sqrt(vv02)
        else:
            if not 0:
                raise AssertionError('Emit function not set up yet')
            else:
                angdist = AngularDist({'type':'costheta',  'altitude':f"0,{np.pi / 2}", 
                 'azimuth':f"0,{2 * np.pi}"}, None)
                VV = angular_distribution(angdist, x1[:, hhh], vv2)
                v1[:, hhh] = VV
                if self.inputs.sticking_info.stickcoef > 0:
                    f1[hhh] *= 1 - self.inputs.sticking_info.stickcoef
                else:
                    assert 0