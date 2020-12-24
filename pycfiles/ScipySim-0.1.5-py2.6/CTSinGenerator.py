# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/math/trig/CTSinGenerator.py
# Compiled at: 2010-04-22 06:03:43
from scipysim.actors import Channel, Source
from sin import Sin
from scipysim.actors.signal import Ramp

class CTSinGenerator(Source):
    """
    This model combines a ramp source with the sin trig function 
    to create a ct sin source.
    """
    output_domains = ('CT', )

    def __init__(self, out, amplitude=1.0, freq=1.0, phi=0.0, timestep=0.001, simulation_time=10):
        super(CTSinGenerator, self).__init__(output_channel=out)
        self.chan = Channel()
        self.ramp = Ramp(self.chan, resolution=1.0 / timestep, simulation_time=simulation_time)
        self.sin = Sin(self.chan, self.output_channel, amplitude=amplitude, freq=freq, phi=phi)

    def process(self):
        components = [
         self.sin, self.ramp]
        [ c.start() for c in components ]
        [ comp.join() for comp in components ]
        self.stop = True