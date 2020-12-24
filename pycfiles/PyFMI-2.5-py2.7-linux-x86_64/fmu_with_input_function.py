# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/examples/fmu_with_input_function.py
# Compiled at: 2018-12-15 16:31:41
import os as O, numpy as N, pylab as p
from pyfmi import load_fmu
curr_dir = O.path.dirname(O.path.abspath(__file__))
path_to_fmus = O.path.join(curr_dir, 'files', 'FMUs')
path_to_fmus_me1 = O.path.join(path_to_fmus, 'ME1.0')
path_to_fmus_cs1 = O.path.join(path_to_fmus, 'CS1.0')

def run_demo(with_plots=True):
    """
    Demonstrates how to simulate an FMU with an input function.
    
    See also simulation_with_input.py
    """
    fmu_name = O.path.join(path_to_fmus_me1, 'SecondOrder.fmu')
    input_object = (
     'u', N.cos)
    model = load_fmu(fmu_name)
    res = model.simulate(final_time=30, input=input_object, options={'ncp': 3000})
    x1_sim = res['x1']
    x2_sim = res['x2']
    u_sim = res['u']
    time_sim = res['time']
    assert N.abs(res.final('x1') - -1.646485144) < 0.001
    assert N.abs(res.final('x2') * 10.0 - -7.30591626709) < 0.001
    assert N.abs(res.final('u') * 10.0 - 1.54251449888) < 0.001
    if with_plots:
        fig = p.figure()
        p.subplot(2, 1, 1)
        p.plot(time_sim, x1_sim, time_sim, x2_sim)
        p.subplot(2, 1, 2)
        p.plot(time_sim, u_sim)
        p.show()


if __name__ == '__main__':
    run_demo()