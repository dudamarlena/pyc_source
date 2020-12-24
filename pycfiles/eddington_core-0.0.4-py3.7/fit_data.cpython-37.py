# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/fit_data.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 442 bytes
from dataclasses import dataclass
import numpy as np

@dataclass
class FitData:
    x: np.ndarray
    xerr: np.ndarray
    y: np.ndarray
    yerr: np.ndarray

    @staticmethod
    def build_from_data_dict(data_dict):
        values = list(data_dict.values())
        return FitData(x=(np.array(values[0])),
          xerr=(np.array(values[1])),
          y=(np.array(values[2])),
          yerr=(np.array(values[3])))