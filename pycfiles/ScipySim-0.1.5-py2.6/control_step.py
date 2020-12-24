# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/control_step.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 7, 2010

brianthorne

"""
from scipysim.actors import Channel, Model, MakeChans
from scipysim.actors.math import Constant
from scipysim.actors.signal import Step
from scipysim.actors.display import Plotter
import scipy, scipy.signal

class ControlStep(Model):
    """This simulation is a P controller responding to a step input."""

    def __init__(self):
        """Create the components"""
        super(ControlStep, self).__init__()
        T = 120
        freq = 50
        dt = 1.0 / freq
        p = 8.0 * scipy.pi
        sys = scipy.signal.lti(p, [1, p])
        yo = scipy.signal.lsim(sys, u, t)
        wires = MakeChans(5)
        src = Constant(wires[0], value=0, resolution=freq, simulation_time=T)
        signal = Step(wires[1], switch_time=60, resolution=50, simulation_time=120)
        dst = Plotter(wires[0])
        dst2 = Plotter(wires[1])
        self.components = [
         src, dst, dst2, signal]


if __name__ == '__main__':
    ControlStep().run()