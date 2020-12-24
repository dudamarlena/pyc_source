# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/preprocessing/sequence.py
# Compiled at: 2019-05-31 02:46:14
# Size of source mod 2**32: 1408 bytes
"""This code is collections of sequence processing toolkits
"""
from __future__ import print_function, division, absolute_import
import numpy as np
from odin.preprocessing.base import Extractor

class _SequenceExtractor(Extractor):
    pass


class MaxLength(_SequenceExtractor):
    __doc__ = ' Sequences longer than this will be filtered out. '

    def __init__(self, max_len=1234, input_name=None):
        super(MaxLength, self).__init__()
        self.max_len = int(max_len)
        self.input_name = input_name

    def _transform(self, X):
        pass


class IndexShift(object):
    __doc__ = ' IndexShift '

    def __init__(self, start_index=None, end_index=None, index_from=None):
        super(IndexShift, self).__init__()


class SkipFrequent(_SequenceExtractor):

    def __init__(self, new):
        pass


class OOVindex(_SequenceExtractor):
    __doc__ = ' Out-of-vocabulary processing\n  Any index that is: < lower or > upper will be replaced\n  by given `oov_index`\n\n  Parameters\n  ----------\n  oov_index : scalar\n    pass\n  lower : {scalar or None}\n    if None, use `min` value of all given sequences\n  upper : {scalar or None}\n    if None, use `max` value of all given sequences\n  input_name : {list of string, None}\n    pass\n  '

    def __init__(self, oov_index, lower=None, upper=None, input_name=None):
        super(OOVindex, self).__init__()
        self.oov_index = int(oov_index)