# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/Gallery/Gallery.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 530 bytes


class Gallery:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self._set_status('running', 'Running Gallery')
        self._set_status('finished', 'Finished Gallery')

    def _set_state(self, **kwargs):
        self.set_state(kwargs)

    def _set_error(self, error_message):
        self._set_status('error', error_message)

    def _set_status(self, status, status_message=''):
        self._set_state(status=status, status_message=status_message)