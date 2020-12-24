# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/examples/producer_sim/example_producer_sim.py
# Compiled at: 2019-06-26 10:31:53
import time, numpy as np
from online_monitor.utils.producer_sim import ProducerSim
from online_monitor.utils import utils

class ExampleProducerSim(ProducerSim):

    def setup_producer_device(self):
        ProducerSim.setup_producer_device(self)
        self.time_stamp = 0

    def send_data(self):
        time.sleep(float(self.config['delay']))
        random_data = {'time_stamp': self.time_stamp, 'position': np.random.randint(0, 10, 10000).reshape((100, 100))}
        self.sender.send_json(random_data, cls=utils.NumpyEncoder)
        self.time_stamp += 1