# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/builders/graph_rewriter_builder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1798 bytes
"""Functions for quantized training and evaluation."""
import tensorflow as tf

def build(graph_rewriter_config, is_training):
    """Returns a function that modifies default graph based on options.

  Args:
    graph_rewriter_config: graph_rewriter_pb2.GraphRewriter proto.
    is_training: whether in training of eval mode.
  """

    def graph_rewrite_fn():
        if graph_rewriter_config.quantization.weight_bits != 8 or graph_rewriter_config.quantization.activation_bits != 8:
            raise ValueError('Only 8bit quantization is supported')
        elif is_training:
            tf.contrib.quantize.experimental_create_training_graph(input_graph=(tf.get_default_graph()),
              quant_delay=(graph_rewriter_config.quantization.delay))
        else:
            tf.contrib.quantize.experimental_create_eval_graph(input_graph=(tf.get_default_graph()))
        tf.contrib.layers.summarize_collection('quant_vars')

    return graph_rewrite_fn