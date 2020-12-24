# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/SpikeForestAnalysis/SpikeForestAnalysis.py
# Compiled at: 2019-11-20 16:46:11
# Size of source mod 2**32: 1151 bytes
import kachery as ka

class SpikeForestAnalysis:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running SpikeForestAnalysis')
        path = state.get('path', None)
        if not path:
            self._set_error('Missing path')
            return
        self._set_status('running', 'Loading object: {}'.format(path))
        obj = ka.load_object(path=path, fr='default_readonly')
        if not obj:
            self._set_error('Unable to load object: {}'.format(path))
        if 'StudyAnalysisResults' in obj:
            del obj['StudyAnalysisResults']
        self._set_state(object=obj)
        self._set_status('finished', 'Finished SpikeForestAnalysis')

    def _set_state(self, **kwargs):
        self.set_state(kwargs)

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self._set_state(status=status, status_message=status_message)