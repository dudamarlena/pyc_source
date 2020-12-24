# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/Surface3d/Surface3d.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 2026 bytes
from mountaintools import client as mt
from mountaintools import client as mt
import numpy as np

class Surface3d:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running surface3D')
        mt.configDownloadFrom(state.get('download_from', []))
        python_state = dict()
        path0 = state.get('faces_path', None)
        if path0:
            x = mt.realizeFile(path0)
            if not x:
                self._set_error('Unable to load file: {}'.format(path0))
                return
            faces0 = np.load(x)
            faces = []
            for j in range(faces0.shape[0]):
                faces.extend([3, faces0[(j, 0)], faces0[(j, 1)], faces0[(j, 2)]])

            faces = np.array(faces)
            python_state['faces'] = faces
        path0 = state.get('vertices_path', None)
        if path0:
            x = mt.realizeFile(path0)
            if not x:
                self._set_error('Unable to load file: {}'.format(path0))
                return
            vertices0 = np.load(x)
            python_state['vertices'] = vertices0.T
        path0 = state.get('scalars_path', None)
        if path0:
            x = mt.realizeFile(path0)
            if not x:
                self._set_error('Unable to load file: {}'.format(path0))
                return
            x = np.load(x)
            python_state['scalars'] = x
        python_state['status'] = 'finished'
        python_state['status_message'] = 'finished'
        self.set_python_state(python_state)

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self.set_python_state(dict(status=status, status_message=status_message))