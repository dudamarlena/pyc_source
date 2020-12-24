# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/NWBFile/NWBFile.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 1486 bytes
from mountaintools import client as mt
import pycommon.nwb_to_dict as nwb_to_dict
from .examples import examples

class NWBFile:
    examples = examples

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running NWBFile')
        mt.configDownloadFrom(state.get('download_from', []))
        path = state.get('path', None)
        if path:
            if path.endswith('.nwb'):
                self._set_status('running', 'Reading nwb file: {}'.format(path))
                obj = nwb_to_dict(path, use_cache=False, exclude_data=True, verbose=False)
                self._set_status('running', 'Finished nwb file: {}'.format(path))
            else:
                self._set_status('running', 'Realizing object: {}'.format(path))
                obj = mt.loadObject(path=path)
            if not obj:
                self._set_error('Unable to realize object: {}'.format(path))
                return
            self.set_python_state(dict(status='finished',
              status_message=('finished loading: {}'.format(path)),
              object=obj))
        else:
            self._set_error('Missing path')

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self.set_python_state(dict(status=status, status_message=status_message))