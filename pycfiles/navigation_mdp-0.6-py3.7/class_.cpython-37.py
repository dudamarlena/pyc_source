# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/navigation_mdp/class_.py
# Compiled at: 2020-04-15 14:20:54
# Size of source mod 2**32: 727 bytes
import numpy as np

class XYClassDistribution:

    def __init__(self, layout, marker_to_class_id=None):
        self.layout = layout
        if marker_to_class_id is None:
            self.marker_to_class_id = {elem:elem for line in layout for elem in line}
        else:
            self.marker_to_class_id = marker_to_class_id
        self.class_layout = self._create_layout(self.layout)

    def _create_layout(self, layout):
        class_layout = []
        for line in layout:
            class_layout.append([])
            for sym in line:
                class_layout[(-1)].append(self.marker_to_class_id[sym])

        return class_layout

    def __call__(self):
        return np.asarray(self.class_layout)