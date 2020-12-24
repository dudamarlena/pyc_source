# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/hyperparams_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 15480 bytes
"""Tests object_detection.core.hyperparams_builder."""
import numpy as np, tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import hyperparams_builder
from object_detection.protos import hyperparams_pb2
slim = tf.contrib.slim

class HyperparamsBuilderTest(tf.test.TestCase):

    def _get_scope_key(self, op):
        return getattr(op, '_key_op', str(op))

    def test_default_arg_scope_has_conv2d_op(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l1_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        self.assertTrue(self._get_scope_key(slim.conv2d) in scope)

    def test_default_arg_scope_has_separable_conv2d_op(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l1_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        self.assertTrue(self._get_scope_key(slim.separable_conv2d) in scope)

    def test_default_arg_scope_has_conv2d_transpose_op(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l1_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        self.assertTrue(self._get_scope_key(slim.conv2d_transpose) in scope)

    def test_explicit_fc_op_arg_scope_has_fully_connected_op(self):
        conv_hyperparams_text_proto = '\n      op: FC\n      regularizer {\n        l1_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        self.assertTrue(self._get_scope_key(slim.fully_connected) in scope)

    def test_separable_conv2d_and_conv2d_and_transpose_have_same_parameters(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l1_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        kwargs_1, kwargs_2, kwargs_3 = scope.values()
        self.assertDictEqual(kwargs_1, kwargs_2)
        self.assertDictEqual(kwargs_1, kwargs_3)

    def test_return_l1_regularized_weights(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l1_regularizer {\n          weight: 0.5\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        regularizer = conv_scope_arguments['weights_regularizer']
        weights = np.array([1.0, -1, 4.0, 2.0])
        with self.test_session() as (sess):
            result = sess.run(regularizer(tf.constant(weights)))
        self.assertAllClose(np.abs(weights).sum() * 0.5, result)

    def test_return_l2_regularizer_weights(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n          weight: 0.42\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        regularizer = conv_scope_arguments['weights_regularizer']
        weights = np.array([1.0, -1, 4.0, 2.0])
        with self.test_session() as (sess):
            result = sess.run(regularizer(tf.constant(weights)))
        self.assertAllClose(np.power(weights, 2).sum() / 2.0 * 0.42, result)

    def test_return_non_default_batch_norm_params_with_train_during_train(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      batch_norm {\n        decay: 0.7\n        center: false\n        scale: true\n        epsilon: 0.03\n        train: true\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['normalizer_fn'], slim.batch_norm)
        batch_norm_params = conv_scope_arguments['normalizer_params']
        self.assertAlmostEqual(batch_norm_params['decay'], 0.7)
        self.assertAlmostEqual(batch_norm_params['epsilon'], 0.03)
        self.assertFalse(batch_norm_params['center'])
        self.assertTrue(batch_norm_params['scale'])
        self.assertTrue(batch_norm_params['is_training'])

    def test_return_batch_norm_params_with_notrain_during_eval(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      batch_norm {\n        decay: 0.7\n        center: false\n        scale: true\n        epsilon: 0.03\n        train: true\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=False)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['normalizer_fn'], slim.batch_norm)
        batch_norm_params = conv_scope_arguments['normalizer_params']
        self.assertAlmostEqual(batch_norm_params['decay'], 0.7)
        self.assertAlmostEqual(batch_norm_params['epsilon'], 0.03)
        self.assertFalse(batch_norm_params['center'])
        self.assertTrue(batch_norm_params['scale'])
        self.assertFalse(batch_norm_params['is_training'])

    def test_return_batch_norm_params_with_notrain_when_train_is_false(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      batch_norm {\n        decay: 0.7\n        center: false\n        scale: true\n        epsilon: 0.03\n        train: false\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['normalizer_fn'], slim.batch_norm)
        batch_norm_params = conv_scope_arguments['normalizer_params']
        self.assertAlmostEqual(batch_norm_params['decay'], 0.7)
        self.assertAlmostEqual(batch_norm_params['epsilon'], 0.03)
        self.assertFalse(batch_norm_params['center'])
        self.assertTrue(batch_norm_params['scale'])
        self.assertFalse(batch_norm_params['is_training'])

    def test_do_not_use_batch_norm_if_default(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['normalizer_fn'], None)
        self.assertEqual(conv_scope_arguments['normalizer_params'], None)

    def test_use_none_activation(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      activation: NONE\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['activation_fn'], None)

    def test_use_relu_activation(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      activation: RELU\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['activation_fn'], tf.nn.relu)

    def test_use_relu_6_activation(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n        }\n      }\n      activation: RELU_6\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        self.assertEqual(conv_scope_arguments['activation_fn'], tf.nn.relu6)

    def _assert_variance_in_range(self, initializer, shape, variance, tol=0.01):
        with tf.Graph().as_default() as (g):
            with self.test_session(graph=g) as (sess):
                var = tf.get_variable(name='test', shape=shape, dtype=tf.float32, initializer=initializer)
                sess.run(tf.global_variables_initializer())
                values = sess.run(var)
                self.assertAllClose(np.var(values), variance, tol, tol)

    def test_variance_in_range_with_variance_scaling_initializer_fan_in(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        variance_scaling_initializer {\n          factor: 2.0\n          mode: FAN_IN\n          uniform: false\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        initializer = conv_scope_arguments['weights_initializer']
        self._assert_variance_in_range(initializer, shape=[100, 40], variance=0.02)

    def test_variance_in_range_with_variance_scaling_initializer_fan_out(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        variance_scaling_initializer {\n          factor: 2.0\n          mode: FAN_OUT\n          uniform: false\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        initializer = conv_scope_arguments['weights_initializer']
        self._assert_variance_in_range(initializer, shape=[100, 40], variance=0.05)

    def test_variance_in_range_with_variance_scaling_initializer_fan_avg(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        variance_scaling_initializer {\n          factor: 2.0\n          mode: FAN_AVG\n          uniform: false\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        initializer = conv_scope_arguments['weights_initializer']
        self._assert_variance_in_range(initializer, shape=[100, 40], variance=0.02857142857142857)

    def test_variance_in_range_with_variance_scaling_initializer_uniform(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        variance_scaling_initializer {\n          factor: 2.0\n          mode: FAN_IN\n          uniform: true\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        initializer = conv_scope_arguments['weights_initializer']
        self._assert_variance_in_range(initializer, shape=[100, 40], variance=0.02)

    def test_variance_in_range_with_truncated_normal_initializer(self):
        conv_hyperparams_text_proto = '\n      regularizer {\n        l2_regularizer {\n        }\n      }\n      initializer {\n        truncated_normal_initializer {\n          mean: 0.0\n          stddev: 0.8\n        }\n      }\n    '
        conv_hyperparams_proto = hyperparams_pb2.Hyperparams()
        text_format.Merge(conv_hyperparams_text_proto, conv_hyperparams_proto)
        scope = hyperparams_builder.build(conv_hyperparams_proto, is_training=True)
        conv_scope_arguments = scope.values()[0]
        initializer = conv_scope_arguments['weights_initializer']
        self._assert_variance_in_range(initializer, shape=[100, 40], variance=0.49, tol=0.1)


if __name__ == '__main__':
    tf.test.main()