# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Zeras/model_template.py
# Compiled at: 2020-03-15 07:46:43
# Size of source mod 2**32: 1855 bytes
"""
Created on Sat Feb 16 07:18:29 2019

@author: limingfan
"""
import tensorflow as tf
from Zeras.model_baseboard import ModelBaseboard

class ModelTemplate(ModelBaseboard):
    __doc__ = ' Template for model graph.\n        Three methods\n        pb/debug tensor names\n    '

    def __init__(self, settings):
        super(ModelTemplate, self).__init__(settings)
        self.pb_input_names = {'input_x': 'input_x:0'}
        self.pb_output_names = {'logits': 'vs_gpu/score/logits:0'}
        self.pb_save_names = ['vs_gpu/score/logits']
        self.debug_tensor_names = [
         'vs_gpu/score/logits:0',
         'vs_gpu/score/logits:0']

    def build_placeholder(self):
        """
        """
        input_x = None
        input_y = None
        input_tensors = {'input_x': input_x}
        label_tensors = {'input_y': input_y}
        return (
         input_tensors, label_tensors)

    def build_inference(self, input_tensors):
        """
        """
        keep_prob = tf.get_variable('keep_prob', shape=[], dtype=(tf.float32), trainable=False)
        print(keep_prob)
        logits_normed = None
        output_tensors = {'logits_normed': logits_normed}
        return output_tensors

    def build_loss_and_metric(self, output_tensors, label_tensors):
        """
        """
        loss_model = None
        metric = None
        loss_metric_tensors = {'loss_model':loss_model, 
         'metric':metric}
        return loss_metric_tensors