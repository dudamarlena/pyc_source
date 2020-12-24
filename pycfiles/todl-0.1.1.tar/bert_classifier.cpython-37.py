# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/modeling/models/bert_classifier.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 3499 bytes
"""Trainer network for BERT-style models."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from official.nlp.modeling import networks

@tf.keras.utils.register_keras_serializable(package='Text')
class BertClassifier(tf.keras.Model):
    __doc__ = 'Classifier model based on a BERT-style transformer-based encoder.\n\n  This is an implementation of the network structure surrounding a transformer\n  encoder as described in "BERT: Pre-training of Deep Bidirectional Transformers\n  for Language Understanding" (https://arxiv.org/abs/1810.04805).\n\n  The BertClassifier allows a user to pass in a transformer stack, and\n  instantiates a classification network based on the passed `num_classes`\n  argument.\n\n  Arguments:\n    network: A transformer network. This network should output a sequence output\n      and a classification output. Furthermore, it should expose its embedding\n      table via a "get_embedding_table" method.\n    num_classes: Number of classes to predict from the classification network.\n    initializer: The initializer (if any) to use in the classification networks.\n      Defaults to a Glorot uniform initializer.\n    output: The output style for this network. Can be either \'logits\' or\n      \'predictions\'.\n  '

    def __init__(self, network, num_classes, initializer='glorot_uniform', output='logits', dropout_rate=0.1, **kwargs):
        self._self_setattr_tracking = False
        self._config = {'network':network, 
         'num_classes':num_classes, 
         'initializer':initializer, 
         'output':output}
        inputs = network.inputs
        _, cls_output = network(inputs)
        cls_output = tf.keras.layers.Dropout(rate=dropout_rate)(cls_output)
        self.classifier = networks.Classification(input_width=(cls_output.shape[(-1)]),
          num_classes=num_classes,
          initializer=initializer,
          output=output,
          name='classification')
        predictions = self.classifier(cls_output)
        (super(BertClassifier, self).__init__)(inputs=inputs, 
         outputs=predictions, **kwargs)

    def get_config(self):
        return self._config

    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)