# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/spikeforest_widgets/generated/spikeforest_widgets/spikeforest_widgets/widgets/Analysis/Analysis.py
# Compiled at: 2019-11-18 14:17:44
# Size of source mod 2**32: 979 bytes
import kachery as ka

class Analysis:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running Analysis')
        path = state.get('path', None)
        if not path:
            self._set_error('Missing path')
            return
        self._set_status('running', 'Loading object: {}'.format(path))
        obj = ka.load_object(path=path, fr='default_readonly')
        if not obj:
            self._set_error('Unable to load object: {}'.format(path))
        self._set_state(object=obj)
        self._set_status('finished', 'Finished Analysis')

    def _set_state(self, **kwargs):
        self.set_state(kwargs)

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self._set_state(status=status, status_message=status_message)