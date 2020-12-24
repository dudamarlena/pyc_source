# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/examples/fmi_bouncing_ball_cs.py
# Compiled at: 2018-12-15 16:31:42
import os as O, pylab as P, numpy as N
from pyfmi import load_fmu
curr_dir = O.path.dirname(O.path.abspath(__file__))
path_to_fmus = O.path.join(curr_dir, 'files', 'FMUs', 'CS1.0')
path_to_fmus2 = O.path.join(curr_dir, 'files', 'FMUs', 'CS2.0')

def run_demo(with_plots=True, version='2.0'):
    """
    Demonstrates how to use PyFMI for simulation of 
    Co-Simulation FMUs (version 1.0 or 2.0).
    """
    if version == '1.0':
        fmu_name = O.path.join(path_to_fmus, 'bouncingBall.fmu')
    else:
        fmu_name = O.path.join(path_to_fmus2, 'bouncingBall.fmu')
    model = load_fmu(fmu_name)
    res = model.simulate(final_time=2.0)
    h_res = res['h']
    v_res = res['v']
    t = res['time']
    assert N.abs(res.final('h') - 0.0424044) < 0.01
    if with_plots:
        fig = P.figure()
        P.clf()
        P.subplot(2, 1, 1)
        P.plot(t, h_res)
        P.ylabel('Height (m)')
        P.xlabel('Time (s)')
        P.subplot(2, 1, 2)
        P.plot(t, v_res)
        P.ylabel('Velocity (m/s)')
        P.xlabel('Time (s)')
        P.suptitle('FMI Bouncing Ball')
        P.show()


if __name__ == '__main__':
    run_demo()