# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/central_limit_theorem.py
# Compiled at: 2010-04-22 06:03:43
from scipysim.actors import Channel, Model, MakeChans
from scipysim.actors.display import Plotter
from scipysim.actors.signal import Ramp, Copier, RandomSource
from scipysim.actors.math import Summer
from scipysim.actors.io import Bundle
from scipysim.actors.display import BundleHistPlotter
import logging
logging.basicConfig(level=logging.INFO)
logging.info('Starting dual ramp + noise sum.')

class MultiSumPlot(Model):
    """
    This example connects N random sources to a summer block
    The final output is plotted AFTER all the processing is complete.
    
    The components are all generating the same sequence of tags, so are always
    synchronised.
    """

    def __init__(self, N=5):
        """Set up the simulation"""
        super(MultiSumPlot, self).__init__()
        wires = MakeChans(N + 2)
        rndSources = [ RandomSource(wires[i], resolution=15) for i in xrange(N) ]
        summer = Summer(wires[:N], wires[N])
        bundler = Bundle(wires[N], wires[(N + 1)])
        dst = BundleHistPlotter(wires[(N + 1)], title='Summing %d Noise sources' % N, show=True)
        self.components = rndSources + [summer, dst, bundler]


if __name__ == '__main__':
    for i in [1, 2, 3, 6, 12, 20]:
        MultiSumPlot(N=i).run()