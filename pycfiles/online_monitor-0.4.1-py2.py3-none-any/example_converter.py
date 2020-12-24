# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/examples/converter/example_converter.py
# Compiled at: 2019-06-26 10:32:16
import zmq, numpy as np
from online_monitor.utils import utils
from online_monitor.converter.transceiver import Transceiver

class ExampleConverter(Transceiver):

    def deserialize_data(self, data):
        return zmq.utils.jsonapi.loads(data, object_hook=utils.json_numpy_obj_hook)

    def interpret_data(self, data):
        data = data[0][1]
        position_with_thr = data['position'].copy()
        position_with_thr[position_with_thr < self.config['threshold']] = 0
        data_with_threshold = {'time_stamp': data['time_stamp'], 'position_with_threshold_%s' % self.name: position_with_thr}
        if np.any(position_with_thr):
            return [data_with_threshold]

    def serialize_data(self, data):
        return zmq.utils.jsonapi.dumps(data, cls=utils.NumpyEncoder)