# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv0d/cipaired.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 695 bytes
import numpy as np
from .. import _base

class FraminghamSystolicBloodPressure(_base.DatasetCIpaired):

    def _set_values(self):
        self.www = 'http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html'
        self.YA = np.array([141, 119, 122, 127, 125, 123, 113, 106, 131, 142, 131, 135, 119, 130, 121], dtype=float)
        self.YB = np.array([168, 111, 139, 127, 155, 115, 125, 123, 130, 137, 130, 129, 112, 141, 122], dtype=float)
        self.alpha = 0.05
        self.mu = 0
        self.ci = (-12.4, 1.8)
        self.note = ('Note     ', 'From "Confidence Intervals for Matched Samples, Continuous Outcome" at the link above.')