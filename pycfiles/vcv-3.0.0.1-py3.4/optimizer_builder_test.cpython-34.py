# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/optimizer_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 6543 bytes
"""Tests for optimizer_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import optimizer_builder
from object_detection.protos import optimizer_pb2

class LearningRateBuilderTest(tf.test.TestCase):

    def testBuildConstantLearningRate(self):
        learning_rate_text_proto = '\n      constant_learning_rate {\n        learning_rate: 0.004\n      }\n    '
        global_summaries = set([])
        learning_rate_proto = optimizer_pb2.LearningRate()
        text_format.Merge(learning_rate_text_proto, learning_rate_proto)
        learning_rate = optimizer_builder._create_learning_rate(learning_rate_proto, global_summaries)
        self.assertAlmostEqual(learning_rate, 0.004)

    def testBuildExponentialDecayLearningRate(self):
        learning_rate_text_proto = '\n      exponential_decay_learning_rate {\n        initial_learning_rate: 0.004\n        decay_steps: 99999\n        decay_factor: 0.85\n        staircase: false\n      }\n    '
        global_summaries = set([])
        learning_rate_proto = optimizer_pb2.LearningRate()
        text_format.Merge(learning_rate_text_proto, learning_rate_proto)
        learning_rate = optimizer_builder._create_learning_rate(learning_rate_proto, global_summaries)
        self.assertTrue(isinstance(learning_rate, tf.Tensor))

    def testBuildManualStepLearningRate(self):
        learning_rate_text_proto = '\n      manual_step_learning_rate {\n        schedule {\n          step: 0\n          learning_rate: 0.006\n        }\n        schedule {\n          step: 90000\n          learning_rate: 0.00006\n        }\n      }\n    '
        global_summaries = set([])
        learning_rate_proto = optimizer_pb2.LearningRate()
        text_format.Merge(learning_rate_text_proto, learning_rate_proto)
        learning_rate = optimizer_builder._create_learning_rate(learning_rate_proto, global_summaries)
        self.assertTrue(isinstance(learning_rate, tf.Tensor))

    def testRaiseErrorOnEmptyLearningRate(self):
        learning_rate_text_proto = '\n    '
        global_summaries = set([])
        learning_rate_proto = optimizer_pb2.LearningRate()
        text_format.Merge(learning_rate_text_proto, learning_rate_proto)
        with self.assertRaises(ValueError):
            optimizer_builder._create_learning_rate(learning_rate_proto, global_summaries)


class OptimizerBuilderTest(tf.test.TestCase):

    def testBuildRMSPropOptimizer(self):
        optimizer_text_proto = '\n      rms_prop_optimizer: {\n        learning_rate: {\n          exponential_decay_learning_rate {\n            initial_learning_rate: 0.004\n            decay_steps: 800720\n            decay_factor: 0.95\n          }\n        }\n        momentum_optimizer_value: 0.9\n        decay: 0.9\n        epsilon: 1.0\n      }\n      use_moving_average: false\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        optimizer = optimizer_builder.build(optimizer_proto, global_summaries)
        self.assertTrue(isinstance(optimizer, tf.train.RMSPropOptimizer))

    def testBuildMomentumOptimizer(self):
        optimizer_text_proto = '\n      momentum_optimizer: {\n        learning_rate: {\n          constant_learning_rate {\n            learning_rate: 0.001\n          }\n        }\n        momentum_optimizer_value: 0.99\n      }\n      use_moving_average: false\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        optimizer = optimizer_builder.build(optimizer_proto, global_summaries)
        self.assertTrue(isinstance(optimizer, tf.train.MomentumOptimizer))

    def testBuildAdamOptimizer(self):
        optimizer_text_proto = '\n      adam_optimizer: {\n        learning_rate: {\n          constant_learning_rate {\n            learning_rate: 0.002\n          }\n        }\n      }\n      use_moving_average: false\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        optimizer = optimizer_builder.build(optimizer_proto, global_summaries)
        self.assertTrue(isinstance(optimizer, tf.train.AdamOptimizer))

    def testBuildMovingAverageOptimizer(self):
        optimizer_text_proto = '\n      adam_optimizer: {\n        learning_rate: {\n          constant_learning_rate {\n            learning_rate: 0.002\n          }\n        }\n      }\n      use_moving_average: True\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        optimizer = optimizer_builder.build(optimizer_proto, global_summaries)
        self.assertTrue(isinstance(optimizer, tf.contrib.opt.MovingAverageOptimizer))

    def testBuildMovingAverageOptimizerWithNonDefaultDecay(self):
        optimizer_text_proto = '\n      adam_optimizer: {\n        learning_rate: {\n          constant_learning_rate {\n            learning_rate: 0.002\n          }\n        }\n      }\n      use_moving_average: True\n      moving_average_decay: 0.2\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        optimizer = optimizer_builder.build(optimizer_proto, global_summaries)
        self.assertTrue(isinstance(optimizer, tf.contrib.opt.MovingAverageOptimizer))
        self.assertAlmostEqual(optimizer._ema._decay, 0.2)

    def testBuildEmptyOptimizer(self):
        optimizer_text_proto = '\n    '
        global_summaries = set([])
        optimizer_proto = optimizer_pb2.Optimizer()
        text_format.Merge(optimizer_text_proto, optimizer_proto)
        with self.assertRaises(ValueError):
            optimizer_builder.build(optimizer_proto, global_summaries)


if __name__ == '__main__':
    tf.test.main()