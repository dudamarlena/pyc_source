# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/NWBView/NWBView.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 1105 bytes
from mountaintools import client as mt
from .h5_to_dict import h5_to_dict

class NWBView:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_python_state(dict(status='running', status_message='Running'))
        mt.configDownloadFrom(state.get('download_from', []))
        path = state.get('path', None)
        if path:
            if path.endswith('.nwb'):
                self.set_python_state(dict(status_message=('Realizing object from nwb file: {}'.format(path))))
                obj = h5_to_dict(path, use_cache=True)
            else:
                self.set_python_state(dict(status_message=('Realizing object: {}'.format(path))))
                obj = mt.loadObject(path=path)
            if not obj:
                self.set_python_state(dict(status='error',
                  status_message=('Unable to realize object: {}'.format(path))))
                return
            state['object'] = obj
            state['status'] = 'finished'
            self.set_python_state(state)