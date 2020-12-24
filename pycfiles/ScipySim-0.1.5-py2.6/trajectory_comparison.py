# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/trajectory_comparison.py
# Compiled at: 2010-04-22 06:03:43
"""
A model based on the bouncing ball example in simulink.
This version compares the fixed-step and discrete-event integrators.
"""
from scipysim.actors import Model, MakeChans
from scipysim.actors.signal import Copier
from scipysim.actors.math import Constant
from scipysim.actors.math import CTIntegratorForwardEuler as Integrator
from scipysim.actors.math import CTIntegratorDE1 as DEIntegrator
from scipysim.actors.display import Stemmer
import logging
logging.basicConfig(level=logging.INFO)
logging.info('Logger enabled')

class ThrownBall(Model):
    """
    A simple example simulation where ...
    """

    def __init__(self):
        """
        A basic simulation that ...
        """
        wires = MakeChans(10)
        gravity = -9.81
        initial_position = 10
        initial_velocity = 15
        self.components = [
         Constant(wires[0], value=gravity, resolution=100, simulation_time=4),
         Copier(wires[0], [wires[1], wires[2]]),
         Integrator(wires[1], wires[3], initial_velocity),
         DEIntegrator(wires[2], wires[4], initial_velocity),
         Integrator(wires[3], wires[5], initial_position),
         DEIntegrator(wires[4], wires[6], initial_position),
         Stemmer(wires[5], title='Displacement (fixed-step integration)', own_fig=True, xlabel='Time (s)', ylabel='(m)'),
         Stemmer(wires[6], title='Displacement (discrete-event integration)', own_fig=True, xlabel='Time (s)', ylabel='(m)')]


if __name__ == '__main__':
    ThrownBall().run()