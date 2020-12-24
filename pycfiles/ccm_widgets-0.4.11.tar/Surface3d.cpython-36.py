# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ccm_widgets/generated/ccm_widgets/ccm_widgets/widgets/Surface3d/Surface3d.py
# Compiled at: 2019-09-21 09:51:39
# Size of source mod 2**32: 249 bytes


class Surface3d:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_state(dict(status='running', status_message='Running'))
        self.set_state(dict(status='finished'))