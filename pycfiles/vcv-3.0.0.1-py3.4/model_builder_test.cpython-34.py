# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/model_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 13240 bytes
"""Tests for object_detection.models.model_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import model_builder
from object_detection.meta_architectures import faster_rcnn_meta_arch
from object_detection.meta_architectures import rfcn_meta_arch
from object_detection.meta_architectures import ssd_meta_arch
from object_detection.models import faster_rcnn_inception_resnet_v2_feature_extractor as frcnn_inc_res
from object_detection.models import faster_rcnn_resnet_v1_feature_extractor as frcnn_resnet_v1
from object_detection.models.ssd_inception_v2_feature_extractor import SSDInceptionV2FeatureExtractor
from object_detection.models.ssd_mobilenet_v1_feature_extractor import SSDMobileNetV1FeatureExtractor
from object_detection.protos import model_pb2
FEATURE_EXTRACTOR_MAPS = {'faster_rcnn_resnet50': frcnn_resnet_v1.FasterRCNNResnet50FeatureExtractor, 
 'faster_rcnn_resnet101': frcnn_resnet_v1.FasterRCNNResnet101FeatureExtractor, 
 'faster_rcnn_resnet152': frcnn_resnet_v1.FasterRCNNResnet152FeatureExtractor}

class ModelBuilderTest(tf.test.TestCase):

    def create_model(self, model_config):
        """Builds a DetectionModel based on the model config.

    Args:
      model_config: A model.proto object containing the config for the desired
        DetectionModel.

    Returns:
      DetectionModel based on the config.
    """
        return model_builder.build(model_config, is_training=True)

    def test_create_ssd_inception_v2_model_from_config(self):
        model_text_proto = "\n      ssd {\n        feature_extractor {\n          type: 'ssd_inception_v2'\n          conv_hyperparams {\n            regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n          }\n        }\n        box_coder {\n          faster_rcnn_box_coder {\n          }\n        }\n        matcher {\n          argmax_matcher {\n          }\n        }\n        similarity_calculator {\n          iou_similarity {\n          }\n        }\n        anchor_generator {\n          ssd_anchor_generator {\n            aspect_ratios: 1.0\n          }\n        }\n        image_resizer {\n          fixed_shape_resizer {\n            height: 320\n            width: 320\n          }\n        }\n        box_predictor {\n          convolutional_box_predictor {\n            conv_hyperparams {\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        loss {\n          classification_loss {\n            weighted_softmax {\n            }\n          }\n          localization_loss {\n            weighted_smooth_l1 {\n            }\n          }\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        model = self.create_model(model_proto)
        self.assertIsInstance(model, ssd_meta_arch.SSDMetaArch)
        self.assertIsInstance(model._feature_extractor, SSDInceptionV2FeatureExtractor)

    def test_create_ssd_mobilenet_v1_model_from_config(self):
        model_text_proto = "\n      ssd {\n        feature_extractor {\n          type: 'ssd_mobilenet_v1'\n          conv_hyperparams {\n            regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n          }\n        }\n        box_coder {\n          faster_rcnn_box_coder {\n          }\n        }\n        matcher {\n          argmax_matcher {\n          }\n        }\n        similarity_calculator {\n          iou_similarity {\n          }\n        }\n        anchor_generator {\n          ssd_anchor_generator {\n            aspect_ratios: 1.0\n          }\n        }\n        image_resizer {\n          fixed_shape_resizer {\n            height: 320\n            width: 320\n          }\n        }\n        box_predictor {\n          convolutional_box_predictor {\n            conv_hyperparams {\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        loss {\n          classification_loss {\n            weighted_softmax {\n            }\n          }\n          localization_loss {\n            weighted_smooth_l1 {\n            }\n          }\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        model = self.create_model(model_proto)
        self.assertIsInstance(model, ssd_meta_arch.SSDMetaArch)
        self.assertIsInstance(model._feature_extractor, SSDMobileNetV1FeatureExtractor)

    def test_create_faster_rcnn_resnet_v1_models_from_config(self):
        model_text_proto = "\n      faster_rcnn {\n        num_classes: 3\n        image_resizer {\n          keep_aspect_ratio_resizer {\n            min_dimension: 600\n            max_dimension: 1024\n          }\n        }\n        feature_extractor {\n          type: 'faster_rcnn_resnet101'\n        }\n        first_stage_anchor_generator {\n          grid_anchor_generator {\n            scales: [0.25, 0.5, 1.0, 2.0]\n            aspect_ratios: [0.5, 1.0, 2.0]\n            height_stride: 16\n            width_stride: 16\n          }\n        }\n        first_stage_box_predictor_conv_hyperparams {\n          regularizer {\n            l2_regularizer {\n            }\n          }\n          initializer {\n            truncated_normal_initializer {\n            }\n          }\n        }\n        initial_crop_size: 14\n        maxpool_kernel_size: 2\n        maxpool_stride: 2\n        second_stage_box_predictor {\n          mask_rcnn_box_predictor {\n            fc_hyperparams {\n              op: FC\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        second_stage_post_processing {\n          batch_non_max_suppression {\n            score_threshold: 0.01\n            iou_threshold: 0.6\n            max_detections_per_class: 100\n            max_total_detections: 300\n          }\n          score_converter: SOFTMAX\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        for extractor_type, extractor_class in FEATURE_EXTRACTOR_MAPS.items():
            model_proto.faster_rcnn.feature_extractor.type = extractor_type
            model = model_builder.build(model_proto, is_training=True)
            self.assertIsInstance(model, faster_rcnn_meta_arch.FasterRCNNMetaArch)
            self.assertIsInstance(model._feature_extractor, extractor_class)

    def test_create_faster_rcnn_inception_resnet_v2_model_from_config(self):
        model_text_proto = "\n      faster_rcnn {\n        num_classes: 3\n        image_resizer {\n          keep_aspect_ratio_resizer {\n            min_dimension: 600\n            max_dimension: 1024\n          }\n        }\n        feature_extractor {\n          type: 'faster_rcnn_inception_resnet_v2'\n        }\n        first_stage_anchor_generator {\n          grid_anchor_generator {\n            scales: [0.25, 0.5, 1.0, 2.0]\n            aspect_ratios: [0.5, 1.0, 2.0]\n            height_stride: 16\n            width_stride: 16\n          }\n        }\n        first_stage_box_predictor_conv_hyperparams {\n          regularizer {\n            l2_regularizer {\n            }\n          }\n          initializer {\n            truncated_normal_initializer {\n            }\n          }\n        }\n        initial_crop_size: 17\n        maxpool_kernel_size: 1\n        maxpool_stride: 1\n        second_stage_box_predictor {\n          mask_rcnn_box_predictor {\n            fc_hyperparams {\n              op: FC\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        second_stage_post_processing {\n          batch_non_max_suppression {\n            score_threshold: 0.01\n            iou_threshold: 0.6\n            max_detections_per_class: 100\n            max_total_detections: 300\n          }\n          score_converter: SOFTMAX\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        model = model_builder.build(model_proto, is_training=True)
        self.assertIsInstance(model, faster_rcnn_meta_arch.FasterRCNNMetaArch)
        self.assertIsInstance(model._feature_extractor, frcnn_inc_res.FasterRCNNInceptionResnetV2FeatureExtractor)

    def test_create_faster_rcnn_model_from_config_with_example_miner(self):
        model_text_proto = "\n      faster_rcnn {\n        num_classes: 3\n        feature_extractor {\n          type: 'faster_rcnn_inception_resnet_v2'\n        }\n        image_resizer {\n          keep_aspect_ratio_resizer {\n            min_dimension: 600\n            max_dimension: 1024\n          }\n        }\n        first_stage_anchor_generator {\n          grid_anchor_generator {\n            scales: [0.25, 0.5, 1.0, 2.0]\n            aspect_ratios: [0.5, 1.0, 2.0]\n            height_stride: 16\n            width_stride: 16\n          }\n        }\n        first_stage_box_predictor_conv_hyperparams {\n          regularizer {\n            l2_regularizer {\n            }\n          }\n          initializer {\n            truncated_normal_initializer {\n            }\n          }\n        }\n        second_stage_box_predictor {\n          mask_rcnn_box_predictor {\n            fc_hyperparams {\n              op: FC\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        hard_example_miner {\n          num_hard_examples: 10\n          iou_threshold: 0.99\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        model = model_builder.build(model_proto, is_training=True)
        self.assertIsNotNone(model._hard_example_miner)

    def test_create_rfcn_resnet_v1_model_from_config(self):
        model_text_proto = "\n      faster_rcnn {\n        num_classes: 3\n        image_resizer {\n          keep_aspect_ratio_resizer {\n            min_dimension: 600\n            max_dimension: 1024\n          }\n        }\n        feature_extractor {\n          type: 'faster_rcnn_resnet101'\n        }\n        first_stage_anchor_generator {\n          grid_anchor_generator {\n            scales: [0.25, 0.5, 1.0, 2.0]\n            aspect_ratios: [0.5, 1.0, 2.0]\n            height_stride: 16\n            width_stride: 16\n          }\n        }\n        first_stage_box_predictor_conv_hyperparams {\n          regularizer {\n            l2_regularizer {\n            }\n          }\n          initializer {\n            truncated_normal_initializer {\n            }\n          }\n        }\n        initial_crop_size: 14\n        maxpool_kernel_size: 2\n        maxpool_stride: 2\n        second_stage_box_predictor {\n          rfcn_box_predictor {\n            conv_hyperparams {\n              op: CONV\n              regularizer {\n                l2_regularizer {\n                }\n              }\n              initializer {\n                truncated_normal_initializer {\n                }\n              }\n            }\n          }\n        }\n        second_stage_post_processing {\n          batch_non_max_suppression {\n            score_threshold: 0.01\n            iou_threshold: 0.6\n            max_detections_per_class: 100\n            max_total_detections: 300\n          }\n          score_converter: SOFTMAX\n        }\n      }"
        model_proto = model_pb2.DetectionModel()
        text_format.Merge(model_text_proto, model_proto)
        for extractor_type, extractor_class in FEATURE_EXTRACTOR_MAPS.items():
            model_proto.faster_rcnn.feature_extractor.type = extractor_type
            model = model_builder.build(model_proto, is_training=True)
            self.assertIsInstance(model, rfcn_meta_arch.RFCNMetaArch)
            self.assertIsInstance(model._feature_extractor, extractor_class)


if __name__ == '__main__':
    tf.test.main()