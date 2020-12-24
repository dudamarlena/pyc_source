# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/detector/process/processor.py
# Compiled at: 2019-01-31 02:47:59
# Size of source mod 2**32: 396 bytes
"""
模型输入前处理，以及模型预测后处理
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
from abc import *

class Processor(abc.ABCMeta):

    @abstractmethod
    def pre_process(self, inputs):
        pass

    @abstractmethod
    def post_process(self, outputs):
        pass