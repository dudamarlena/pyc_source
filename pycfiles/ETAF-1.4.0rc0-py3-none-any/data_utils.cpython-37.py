# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/utils/data_utils.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1036 bytes
import numpy
from federatedml.feature.sparse_vector import SparseVector

def dataset_to_list(src):
    if isinstance(src, numpy.ndarray):
        return src.tolist()
    if isinstance(src, list):
        return src
    if isinstance(src, SparseVector):
        vector = [
         0] * src.get_shape()
        for idx, v in src.get_all_data():
            vector[idx] = v

        return vector
    return [src]