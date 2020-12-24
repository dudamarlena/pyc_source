# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/harutaka/Desktop/projects/mlflow-extend/build/lib/mlflow_extend/typing.py
# Compiled at: 2020-02-29 05:57:41
# Size of source mod 2**32: 139 bytes
from typing import Union
import numpy as np, pandas as pd
ArrayLike = Union[(list, tuple, set, np.ndarray, pd.Series, pd.DataFrame)]