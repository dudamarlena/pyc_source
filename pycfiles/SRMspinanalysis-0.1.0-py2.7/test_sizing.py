# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/SRMspinanalysis/tests/test_sizing.py
# Compiled at: 2018-04-25 20:04:38
from .. import sizing
import numpy as np

def test_compute_total_impulse_1():
    spin_rate = 25.0
    roll_inertia = 1.0
    radial_distance = 0.175
    exp = 142.857
    obs = sizing.compute_total_impulse(spin_rate, roll_inertia, radial_distance)
    assert np.allclose(exp, obs)


def test_compute_total_impulse_2():
    spin_rate = 1.0
    roll_inertia = 1.0
    radial_distance = 1.0
    exp = 1.0
    obs = sizing.compute_total_impulse(spin_rate, roll_inertia, radial_distance)
    assert np.allclose(exp, obs)