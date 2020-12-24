# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/matcher_builder.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2100 bytes
"""A function to build an object detection matcher from configuration."""
from object_detection.matchers import argmax_matcher
from object_detection.matchers import bipartite_matcher
from object_detection.protos import matcher_pb2

def build(matcher_config):
    """Builds a matcher object based on the matcher config.

  Args:
    matcher_config: A matcher.proto object containing the config for the desired
      Matcher.

  Returns:
    Matcher based on the config.

  Raises:
    ValueError: On empty matcher proto.
  """
    if not isinstance(matcher_config, matcher_pb2.Matcher):
        raise ValueError('matcher_config not of type matcher_pb2.Matcher.')
    if matcher_config.WhichOneof('matcher_oneof') == 'argmax_matcher':
        matcher = matcher_config.argmax_matcher
        matched_threshold = unmatched_threshold = None
        if not matcher.ignore_thresholds:
            matched_threshold = matcher.matched_threshold
            unmatched_threshold = matcher.unmatched_threshold
        return argmax_matcher.ArgMaxMatcher(matched_threshold=matched_threshold, unmatched_threshold=unmatched_threshold, negatives_lower_than_unmatched=matcher.negatives_lower_than_unmatched, force_match_for_each_row=matcher.force_match_for_each_row)
    if matcher_config.WhichOneof('matcher_oneof') == 'bipartite_matcher':
        return bipartite_matcher.GreedyBipartiteMatcher()
    raise ValueError('Empty matcher.')