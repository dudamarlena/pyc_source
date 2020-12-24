# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/magland/src/ccm_widgets/generated/ccm_widgets/ccm_widgets/widgets/Surface3d/Surface3d.py
# Compiled at: 2019-09-21 09:51:39
# Size of source mod 2**32: 249 bytes


class Surface3d:

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_state(dict(status='running', status_message='Running'))
        self.set_state(dict(status='finished'))