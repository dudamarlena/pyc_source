# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/CorticalSurface/CorticalSurface.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 2260 bytes
from vtk import vtkXMLPolyDataReader
import pycommon.nwb_to_dict as nwb_to_dict
from mountaintools import client as mt
import numpy as np
from .examples import examples

class CorticalSurface:
    examples = examples

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_python_state(dict(status='running', status_message='Running'))
        download_from = state.get('download_from', [])
        path = state.get('path', None)
        name = state.get('name', None)
        if path and name:
            mt.configDownloadFrom(download_from)
            if path.endswith('.nwb'):
                self.set_python_state(dict(status_message=('Realizing object from nwb file: {}'.format(path))))
                obj = nwb_to_dict(path, use_cache=True)
            else:
                self.set_python_state(dict(status_message=('Realizing object: {}'.format(path))))
                obj = mt.loadObject(path=path)
            if not obj:
                self.set_python_state(dict(status='error',
                  status_message=('Unable to realize object: {}'.format(path))))
                return
            datasets = obj['general']['subject']['cortical_surfaces'][name]['_datasets']
            faces0 = np.load(mt.realizeFile(datasets['faces']['_data']))
            vertices = np.load(mt.realizeFile(datasets['vertices']['_data'])).T
            faces = []
            for j in range(faces0.shape[0]):
                faces.extend([3, faces0[(j, 0)], faces0[(j, 1)], faces0[(j, 2)]])

            faces = np.array(faces)
            self.set_python_state(dict(faces=faces,
              vertices=vertices,
              status='finished',
              status_message='Done.'))
        else:
            self.set_python_state(dict(status='error',
              status_message='Missing path and/or name'))