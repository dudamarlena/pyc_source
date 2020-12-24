# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/examples/fmu_with_input.py
# Compiled at: 2018-12-15 16:31:41
import os as O, numpy as N, pylab as p
from pyfmi import load_fmu
curr_dir = O.path.dirname(O.path.abspath(__file__))
path_to_fmus = O.path.join(curr_dir, 'files', 'FMUs')
path_to_fmus_me1 = O.path.join(path_to_fmus, 'ME1.0')
path_to_fmus_cs1 = O.path.join(path_to_fmus, 'CS1.0')

def run_demo(with_plots=True):
    """
    Demonstrates how to simulate an FMU with inputs.
    
    See also simulation_with_input.py
    """
    fmu_name = O.path.join(path_to_fmus_me1, 'SecondOrder.fmu')
    t = N.linspace(0.0, 10.0, 100)
    u = N.cos(t)
    u_traj = N.transpose(N.vstack((t, u)))
    input_object = (
     'u', u_traj)
    model = load_fmu(fmu_name)
    model.set('u', u[0])
    res = model.simulate(final_time=30, input=input_object, options={'ncp': 3000})
    x1_sim = res['x1']
    x2_sim = res['x2']
    u_sim = res['u']
    time_sim = res['time']
    assert N.abs(res.final('x1') * 10.0 - -8.399964) < 0.001
    assert N.abs(res.final('x2') * 10.0 - -5.0691179) < 0.001
    assert N.abs(res.final('u') * 10.0 - -8.3907153) < 0.001
    if with_plots:
        fig = p.figure()
        p.subplot(2, 1, 1)
        p.plot(time_sim, x1_sim, time_sim, x2_sim)
        p.subplot(2, 1, 2)
        p.plot(time_sim, u_sim, 'x-', t, u[:], 'x-')
        p.show()


if __name__ == '__main__':
    run_demo()