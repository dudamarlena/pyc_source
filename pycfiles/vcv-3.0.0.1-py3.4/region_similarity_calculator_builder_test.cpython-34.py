# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/region_similarity_calculator_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2657 bytes
"""Tests for region_similarity_calculator_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import region_similarity_calculator_builder
from object_detection.core import region_similarity_calculator
from object_detection.protos import region_similarity_calculator_pb2 as sim_calc_pb2

class RegionSimilarityCalculatorBuilderTest(tf.test.TestCase):

    def testBuildIoaSimilarityCalculator(self):
        similarity_calc_text_proto = '\n      ioa_similarity {\n      }\n    '
        similarity_calc_proto = sim_calc_pb2.RegionSimilarityCalculator()
        text_format.Merge(similarity_calc_text_proto, similarity_calc_proto)
        similarity_calc = region_similarity_calculator_builder.build(similarity_calc_proto)
        self.assertTrue(isinstance(similarity_calc, region_similarity_calculator.IoaSimilarity))

    def testBuildIouSimilarityCalculator(self):
        similarity_calc_text_proto = '\n      iou_similarity {\n      }\n    '
        similarity_calc_proto = sim_calc_pb2.RegionSimilarityCalculator()
        text_format.Merge(similarity_calc_text_proto, similarity_calc_proto)
        similarity_calc = region_similarity_calculator_builder.build(similarity_calc_proto)
        self.assertTrue(isinstance(similarity_calc, region_similarity_calculator.IouSimilarity))

    def testBuildNegSqDistSimilarityCalculator(self):
        similarity_calc_text_proto = '\n      neg_sq_dist_similarity {\n      }\n    '
        similarity_calc_proto = sim_calc_pb2.RegionSimilarityCalculator()
        text_format.Merge(similarity_calc_text_proto, similarity_calc_proto)
        similarity_calc = region_similarity_calculator_builder.build(similarity_calc_proto)
        self.assertTrue(isinstance(similarity_calc, region_similarity_calculator.NegSqDistSimilarity))


if __name__ == '__main__':
    tf.test.main()