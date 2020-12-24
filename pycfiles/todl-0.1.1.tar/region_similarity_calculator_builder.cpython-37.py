# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/builders/region_similarity_calculator_builder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2383 bytes
"""Builder for region similarity calculators."""
from object_detection.core import region_similarity_calculator
from object_detection.protos import region_similarity_calculator_pb2

def build(region_similarity_calculator_config):
    """Builds region similarity calculator based on the configuration.

  Builds one of [IouSimilarity, IoaSimilarity, NegSqDistSimilarity] objects. See
  core/region_similarity_calculator.proto for details.

  Args:
    region_similarity_calculator_config: RegionSimilarityCalculator
      configuration proto.

  Returns:
    region_similarity_calculator: RegionSimilarityCalculator object.

  Raises:
    ValueError: On unknown region similarity calculator.
  """
    if not isinstance(region_similarity_calculator_config, region_similarity_calculator_pb2.RegionSimilarityCalculator):
        raise ValueError('region_similarity_calculator_config not of type region_similarity_calculator_pb2.RegionsSimilarityCalculator')
    similarity_calculator = region_similarity_calculator_config.WhichOneof('region_similarity')
    if similarity_calculator == 'iou_similarity':
        return region_similarity_calculator.IouSimilarity()
    if similarity_calculator == 'ioa_similarity':
        return region_similarity_calculator.IoaSimilarity()
    if similarity_calculator == 'neg_sq_dist_similarity':
        return region_similarity_calculator.NegSqDistSimilarity()
    if similarity_calculator == 'thresholded_iou_similarity':
        return region_similarity_calculator.ThresholdedIouSimilarity(region_similarity_calculator_config.thresholded_iou_similarity.iou_threshold)
    raise ValueError('Unknown region similarity calculator.')