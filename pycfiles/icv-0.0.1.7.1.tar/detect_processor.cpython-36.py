# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/detector/process/detect_processor.py
# Compiled at: 2019-07-22 04:00:30
# Size of source mod 2**32: 440 bytes
from .processor import Processor
from ...utils import base64_to_np

class DetectionProcessor(Processor):

    @classmethod
    def pre_process(self, inputs):
        return base64_to_np(inputs)

    @classmethod
    def post_process(self, outputs):
        if isinstance(outputs, list):
            outputs = [_.to_json() for _ in outputs]
        else:
            outputs = outputs.to_json()
        return outputs