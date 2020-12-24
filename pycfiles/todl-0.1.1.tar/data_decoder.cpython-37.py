# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/core/data_decoder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1472 bytes
"""Interface for data decoders.

Data decoders decode the input data and return a dictionary of tensors keyed by
the entries in core.reader.Fields.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from abc import ABCMeta
from abc import abstractmethod
import six

class DataDecoder(six.with_metaclass(ABCMeta, object)):
    __doc__ = 'Interface for data decoders.'

    @abstractmethod
    def decode(self, data):
        """Return a single image and associated labels.

    Args:
      data: a string tensor holding a serialized protocol buffer corresponding
        to data for a single image.

    Returns:
      tensor_dict: a dictionary containing tensors. Possible keys are defined in
          reader.Fields.
    """
        pass