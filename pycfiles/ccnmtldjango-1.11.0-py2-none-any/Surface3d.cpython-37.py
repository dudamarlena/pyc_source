# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/magland/src/ccm_widgets/generated/ccm_widgets/ccm_widgets/widgets/Surface3d/Surface3d.py
# Compiled at: 2019-09-05 16:40:35
# Size of source mod 2**32: 446 bytes
from reactopya import Component
from mountaintools import client as mt
import base64
from vtk.util.numpy_support import vtk_to_numpy
from vtk import vtkXMLPolyDataReader

class Surface3d(Component):

    def __init__(self):
        super().__init__()

    def javascript_state_changed(self, prev_state, state):
        self.set_python_state(dict(status='running', status_message='Running'))
        self.set_python_state(dict(status='finished'))