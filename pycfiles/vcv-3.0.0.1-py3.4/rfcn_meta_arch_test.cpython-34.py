# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/meta_architectures/rfcn_meta_arch_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 1768 bytes
"""Tests for object_detection.meta_architectures.rfcn_meta_arch."""
import tensorflow as tf
from object_detection.meta_architectures import faster_rcnn_meta_arch_test_lib
from object_detection.meta_architectures import rfcn_meta_arch

class RFCNMetaArchTest(faster_rcnn_meta_arch_test_lib.FasterRCNNMetaArchTestBase):

    def _get_second_stage_box_predictor_text_proto(self):
        box_predictor_text_proto = '\n      rfcn_box_predictor {\n        conv_hyperparams {\n          op: CONV\n          activation: NONE\n          regularizer {\n            l2_regularizer {\n              weight: 0.0005\n            }\n          }\n          initializer {\n            variance_scaling_initializer {\n              factor: 1.0\n              uniform: true\n              mode: FAN_AVG\n            }\n          }\n        }\n      }\n    '
        return box_predictor_text_proto

    def _get_model(self, box_predictor, **common_kwargs):
        return rfcn_meta_arch.RFCNMetaArch(second_stage_rfcn_box_predictor=box_predictor, **common_kwargs)


if __name__ == '__main__':
    tf.test.main()