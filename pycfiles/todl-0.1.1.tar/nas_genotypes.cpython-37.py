# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/deeplab/core/nas_genotypes.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1792 bytes
"""Genotypes used by NAS."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow.contrib as contrib_slim
from deeplab.core import nas_cell
slim = contrib_slim

class PNASCell(nas_cell.NASBaseCell):
    __doc__ = 'Configuration and construction of the PNASNet-5 Cell.'

    def __init__(self, num_conv_filters, drop_path_keep_prob, total_num_cells, total_training_steps, batch_norm_fn=slim.batch_norm):
        operations = [
         'separable_5x5_2', 'max_pool_3x3', 'separable_7x7_2', 'max_pool_3x3',
         'separable_5x5_2', 'separable_3x3_2', 'separable_3x3_2', 'max_pool_3x3',
         'separable_3x3_2', 'none']
        used_hiddenstates = [
         1, 1, 0, 0, 0, 0, 0]
        hiddenstate_indices = [1, 1, 0, 0, 0, 0, 4, 0, 1, 0]
        super(PNASCell, self).__init__(num_conv_filters, operations, used_hiddenstates, hiddenstate_indices, drop_path_keep_prob, total_num_cells, total_training_steps, batch_norm_fn)