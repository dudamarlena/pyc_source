# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/losses_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 10316 bytes
"""Tests for losses_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import losses_builder
from object_detection.core import losses
from object_detection.protos import losses_pb2

class LocalizationLossBuilderTest(tf.test.TestCase):

    def test_build_weighted_l2_localization_loss(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, localization_loss, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(localization_loss, losses.WeightedL2LocalizationLoss))

    def test_build_weighted_smooth_l1_localization_loss(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_smooth_l1 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, localization_loss, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(localization_loss, losses.WeightedSmoothL1LocalizationLoss))

    def test_build_weighted_iou_localization_loss(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_iou {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, localization_loss, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(localization_loss, losses.WeightedIOULocalizationLoss))

    def test_anchorwise_output(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_smooth_l1 {\n          anchorwise_output: true\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, localization_loss, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(localization_loss, losses.WeightedSmoothL1LocalizationLoss))
        predictions = tf.constant([[[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]])
        targets = tf.constant([[[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]])
        weights = tf.constant([[1.0, 1.0]])
        loss = localization_loss(predictions, targets, weights=weights)
        self.assertEqual(loss.shape, [1, 2])

    def test_raise_error_on_empty_localization_config(self):
        losses_text_proto = '\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        with self.assertRaises(ValueError):
            losses_builder._build_localization_loss(losses_proto)


class ClassificationLossBuilderTest(tf.test.TestCase):

    def test_build_weighted_sigmoid_classification_loss(self):
        losses_text_proto = '\n      classification_loss {\n        weighted_sigmoid {\n        }\n      }\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        classification_loss, _, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(classification_loss, losses.WeightedSigmoidClassificationLoss))

    def test_build_weighted_softmax_classification_loss(self):
        losses_text_proto = '\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        classification_loss, _, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(classification_loss, losses.WeightedSoftmaxClassificationLoss))

    def test_build_bootstrapped_sigmoid_classification_loss(self):
        losses_text_proto = '\n      classification_loss {\n        bootstrapped_sigmoid {\n          alpha: 0.5\n        }\n      }\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        classification_loss, _, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(classification_loss, losses.BootstrappedSigmoidClassificationLoss))

    def test_anchorwise_output(self):
        losses_text_proto = '\n      classification_loss {\n        weighted_sigmoid {\n          anchorwise_output: true\n        }\n      }\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        classification_loss, _, _, _, _ = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(classification_loss, losses.WeightedSigmoidClassificationLoss))
        predictions = tf.constant([[[0.0, 1.0, 0.0], [0.0, 0.5, 0.5]]])
        targets = tf.constant([[[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]])
        weights = tf.constant([[1.0, 1.0]])
        loss = classification_loss(predictions, targets, weights=weights)
        self.assertEqual(loss.shape, [1, 2])

    def test_raise_error_on_empty_config(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        with self.assertRaises(ValueError):
            losses_builder.build(losses_proto)


class HardExampleMinerBuilderTest(tf.test.TestCase):

    def test_do_not_build_hard_example_miner_by_default(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, _, _, _, hard_example_miner = losses_builder.build(losses_proto)
        self.assertEqual(hard_example_miner, None)

    def test_build_hard_example_miner_for_classification_loss(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n      hard_example_miner {\n        loss_type: CLASSIFICATION\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, _, _, _, hard_example_miner = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(hard_example_miner, losses.HardExampleMiner))
        self.assertEqual(hard_example_miner._loss_type, 'cls')

    def test_build_hard_example_miner_for_localization_loss(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n      hard_example_miner {\n        loss_type: LOCALIZATION\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, _, _, _, hard_example_miner = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(hard_example_miner, losses.HardExampleMiner))
        self.assertEqual(hard_example_miner._loss_type, 'loc')

    def test_build_hard_example_miner_with_non_default_values(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n      hard_example_miner {\n        num_hard_examples: 32\n        iou_threshold: 0.5\n        loss_type: LOCALIZATION\n        max_negatives_per_positive: 10\n        min_negatives_per_image: 3\n      }\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        _, _, _, _, hard_example_miner = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(hard_example_miner, losses.HardExampleMiner))
        self.assertEqual(hard_example_miner._num_hard_examples, 32)
        self.assertAlmostEqual(hard_example_miner._iou_threshold, 0.5)
        self.assertEqual(hard_example_miner._max_negatives_per_positive, 10)
        self.assertEqual(hard_example_miner._min_negatives_per_image, 3)


class LossBuilderTest(tf.test.TestCase):

    def test_build_all_loss_parameters(self):
        losses_text_proto = '\n      localization_loss {\n        weighted_l2 {\n        }\n      }\n      classification_loss {\n        weighted_softmax {\n        }\n      }\n      hard_example_miner {\n      }\n      classification_weight: 0.8\n      localization_weight: 0.2\n    '
        losses_proto = losses_pb2.Loss()
        text_format.Merge(losses_text_proto, losses_proto)
        classification_loss, localization_loss, classification_weight, localization_weight, hard_example_miner = losses_builder.build(losses_proto)
        self.assertTrue(isinstance(hard_example_miner, losses.HardExampleMiner))
        self.assertTrue(isinstance(classification_loss, losses.WeightedSoftmaxClassificationLoss))
        self.assertTrue(isinstance(localization_loss, losses.WeightedL2LocalizationLoss))
        self.assertAlmostEqual(classification_weight, 0.8)
        self.assertAlmostEqual(localization_weight, 0.2)


if __name__ == '__main__':
    tf.test.main()