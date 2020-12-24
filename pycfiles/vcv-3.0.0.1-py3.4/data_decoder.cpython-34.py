# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/core/data_decoder.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 1349 bytes
"""Interface for data decoders.

Data decoders decode the input data and return a dictionary of tensors keyed by
the entries in core.reader.Fields.
"""
from abc import ABCMeta
from abc import abstractmethod

class DataDecoder(object):
    __doc__ = 'Interface for data decoders.'
    __metaclass__ = ABCMeta

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