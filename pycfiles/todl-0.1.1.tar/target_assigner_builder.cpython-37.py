# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/builders/target_assigner_builder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1715 bytes
"""A function to build an object detection box coder from configuration."""
from object_detection.builders import box_coder_builder
from object_detection.builders import matcher_builder
from object_detection.builders import region_similarity_calculator_builder
from object_detection.core import target_assigner

def build(target_assigner_config):
    """Builds a TargetAssigner object based on the config.

  Args:
    target_assigner_config: A target_assigner proto message containing config
      for the desired target assigner.

  Returns:
    TargetAssigner object based on the config.
  """
    matcher_instance = matcher_builder.build(target_assigner_config.matcher)
    similarity_calc_instance = region_similarity_calculator_builder.build(target_assigner_config.similarity_calculator)
    box_coder = box_coder_builder.build(target_assigner_config.box_coder)
    return target_assigner.TargetAssigner(matcher=matcher_instance,
      similarity_calc=similarity_calc_instance,
      box_coder_instance=box_coder)