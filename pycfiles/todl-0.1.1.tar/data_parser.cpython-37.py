# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/core/data_parser.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1645 bytes
"""Interface for data parsers.

Data parser parses input data and returns a dictionary of numpy arrays
keyed by the entries in standard_fields.py. Since the parser parses records
to numpy arrays (materialized tensors) directly, it is used to read data for
evaluation/visualization; to parse the data during training, DataDecoder should
be used.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from abc import ABCMeta
from abc import abstractmethod
import six

class DataToNumpyParser(six.with_metaclass(ABCMeta, object)):
    __doc__ = 'Abstract interface for data parser that produces numpy arrays.'

    @abstractmethod
    def parse(self, input_data):
        """Parses input and returns a numpy array or a dictionary of numpy arrays.

    Args:
      input_data: an input data

    Returns:
      A numpy array or a dictionary of numpy arrays or None, if input
      cannot be parsed.
    """
        pass