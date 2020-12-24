# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/spikeforest_widgets/generated/spikeforest_widgets/spikeforest_widgets/widgets/StudySets/StudySets.py
# Compiled at: 2019-11-18 14:07:25
# Size of source mod 2**32: 647 bytes


class StudySets:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running StudySets')
        self._set_status('finished', 'Finished StudySets')

    def _set_state(self, **kwargs):
        self.set_state(kwargs)

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self._set_state(status=status, status_message=status_message)