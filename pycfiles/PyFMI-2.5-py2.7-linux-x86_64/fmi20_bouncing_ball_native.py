# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfmi/examples/fmi20_bouncing_ball_native.py
# Compiled at: 2018-12-15 16:31:41
import os as O, pylab as P, numpy as N
from pyfmi import load_fmu
curr_dir = O.path.dirname(O.path.abspath(__file__))
path_to_fmus = O.path.join(curr_dir, 'files', 'FMUs')
path_to_fmus_me2 = O.path.join(path_to_fmus, 'ME2.0')
path_to_fmus_cs2 = O.path.join(path_to_fmus, 'CS2.0')

def run_demo(with_plots=True):
    """
    This example shows how to use the raw (JModelica.org) FMI interface for
    simulation of an FMU.
    
    FMU = bouncingBall.fmu 
    (Generated using Qtronic FMU SDK (http://www.qtronic.de/en/fmusdk.html) )
    
    This example is written similar to the example in the documentation of the 
    'Functional Mock-up Interface for Model Exchange' version 2.0 
    (http://www.functional-mockup-interface.org/) 
    """
    bouncing_fmu = load_fmu('bouncingBall.fmu', path_to_fmus_me2)
    Tstart = 0.5
    Tend = 3.0
    bouncing_fmu.setup_experiment(start_time=Tstart)
    bouncing_fmu.enter_initialization_mode()
    bouncing_fmu.exit_initialization_mode()
    eInfo = bouncing_fmu.get_event_info()
    eInfo.newDiscreteStatesNeeded = True
    while eInfo.newDiscreteStatesNeeded == True:
        bouncing_fmu.enter_event_mode()
        bouncing_fmu.event_update()
        eInfo = bouncing_fmu.get_event_info()

    bouncing_fmu.enter_continuous_time_mode()
    x = bouncing_fmu.continuous_states
    x_nominal = bouncing_fmu.nominal_continuous_states
    event_ind = bouncing_fmu.get_event_indicators()
    vref = [
     bouncing_fmu.get_variable_valueref('h')] + [bouncing_fmu.get_variable_valueref('v')]
    t_sol = [
     Tstart]
    sol = [bouncing_fmu.get_real(vref)]
    time = Tstart
    Tnext = Tend
    dt = 0.01
    while time < Tend and not bouncing_fmu.get_event_info().terminateSimulation:
        dx = bouncing_fmu.get_derivatives()
        h = min(dt, Tnext - time)
        time = time + h
        bouncing_fmu.time = time
        x = x + h * dx
        bouncing_fmu.continuous_states = x
        event_ind_new = bouncing_fmu.get_event_indicators()
        step_event = bouncing_fmu.completed_integrator_step()
        time_event = abs(time - Tnext) <= 1e-10
        state_event = True if True in ((event_ind_new > 0.0) != (event_ind > 0.0)) else False
        if step_event or time_event or state_event:
            bouncing_fmu.enter_event_mode()
            eInfo = bouncing_fmu.get_event_info()
            eInfo.newDiscreteStatesNeeded = True
            while eInfo.newDiscreteStatesNeeded:
                bouncing_fmu.event_update(intermediateResult=True)
                eInfo = bouncing_fmu.get_event_info()
                if eInfo.newDiscreteStatesNeeded:
                    continue

            if eInfo.valuesOfContinuousStatesChanged:
                x = bouncing_fmu.continuous_states
            if eInfo.nominalsOfContinuousStatesChanged:
                atol = 0.01 * rtol * bouncing_fmu.nominal_continuous_states
            if eInfo.nextEventTimeDefined:
                Tnext = min(eInfo.nextEventTime, Tend)
            else:
                Tnext = Tend
            bouncing_fmu.enter_continuous_time_mode()
        event_ind = event_ind_new
        t_sol += [time]
        sol += [bouncing_fmu.get_real(vref)]

    if with_plots:
        P.figure(1)
        P.plot(t_sol, N.array(sol)[:, 0])
        P.title(bouncing_fmu.get_name())
        P.ylabel('Height (m)')
        P.xlabel('Time (s)')
        P.figure(2)
        P.plot(t_sol, N.array(sol)[:, 1])
        P.title(bouncing_fmu.get_name())
        P.ylabel('Velocity (m/s)')
        P.xlabel('Time (s)')
        P.show()


if __name__ == '__main__':
    run_demo()