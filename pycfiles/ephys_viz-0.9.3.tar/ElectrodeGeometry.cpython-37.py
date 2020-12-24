# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/ElectrodeGeometry/ElectrodeGeometry.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 1561 bytes
import numpy as np
from mountaintools import client as mt
import spikeextractors as se
from .examples import examples

class ElectrodeGeometry:
    examples = examples

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_python_state(dict(status='running', status_message='Running'))
        mt.configDownloadFrom(state.get('download_from', []))
        path = state.get('path', None)
        if path:
            self.set_python_state(dict(status_message=('Realizing file: {}'.format(path))))
            if path.endswith('.csv'):
                path2 = mt.realizeFile(path)
                if not path2:
                    self.set_python_state(dict(status='error',
                      status_message=('Unable to realize file: {}'.format(path))))
                    return
                self.set_python_state(dict(status_message='Loading locatoins'))
                x = np.genfromtxt(path2, delimiter=',')
                locations = x.T
                num_elec = x.shape[0]
                labels = ['{}'.format(a) for a in range(1, num_elec + 1)]
            else:
                raise Exception('Unexpected file type for {}'.format(path))
        else:
            locations = [
             [
              0, 0], [1, 0], [1, 1], [2, 1]]
            labels = ['1', '2', '3', '4']
        state = dict()
        state['locations'] = locations
        state['labels'] = labels
        state['status'] = 'finished'
        self.set_python_state(state)