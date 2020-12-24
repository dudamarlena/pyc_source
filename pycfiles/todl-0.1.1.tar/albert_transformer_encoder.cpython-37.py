# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/modeling/networks/albert_transformer_encoder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 7820 bytes
"""ALBERT (https://arxiv.org/abs/1810.04805) text encoder network."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow.python.keras.engine import network
from official.modeling import activations
from official.nlp.modeling import layers

@tf.keras.utils.register_keras_serializable(package='Text')
class AlbertTransformerEncoder(network.Network):
    __doc__ = 'ALBERT (https://arxiv.org/abs/1810.04805) text encoder network.\n\n  This network implements the encoder described in the paper "ALBERT: A Lite\n  BERT for Self-supervised Learning of Language Representations"\n  (https://arxiv.org/abs/1909.11942).\n\n  Compared with BERT (https://arxiv.org/abs/1810.04805), ALBERT refactorizes\n  embedding parameters into two smaller matrices and shares parameters\n  across layers.\n\n  The default values for this object are taken from the ALBERT-Base\n  implementation described in the paper.\n\n  Arguments:\n    vocab_size: The size of the token vocabulary.\n    embedding_width: The width of the word embeddings. If the embedding width\n      is not equal to hidden size, embedding parameters will be factorized into\n      two matrices in the shape of [\'vocab_size\', \'embedding_width\'] and\n      [\'embedding_width\', \'hidden_size\'] (\'embedding_width\' is usually much\n      smaller than \'hidden_size\').\n    hidden_size: The size of the transformer hidden layers.\n    num_layers: The number of transformer layers.\n    num_attention_heads: The number of attention heads for each transformer. The\n      hidden size must be divisible by the number of attention heads.\n    sequence_length: The sequence length that this encoder expects. If None, the\n      sequence length is dynamic; if an integer, the encoder will require\n      sequences padded to this length.\n    max_sequence_length: The maximum sequence length that this encoder can\n      consume. If None, max_sequence_length uses the value from sequence length.\n      This determines the variable shape for positional embeddings.\n    type_vocab_size: The number of types that the \'type_ids\' input can take.\n    intermediate_size: The intermediate size for the transformer layers.\n    activation: The activation to use for the transformer layers.\n    dropout_rate: The dropout rate to use for the transformer layers.\n    attention_dropout_rate: The dropout rate to use for the attention layers\n      within the transformer layers.\n    initializer: The initialzer to use for all weights in this encoder.\n  '

    def __init__(self, vocab_size, embedding_width=128, hidden_size=768, num_layers=12, num_attention_heads=12, sequence_length=512, max_sequence_length=None, type_vocab_size=16, intermediate_size=3072, activation=activations.gelu, dropout_rate=0.1, attention_dropout_rate=0.1, initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02), **kwargs):
        activation = tf.keras.activations.get(activation)
        initializer = tf.keras.initializers.get(initializer)
        if not max_sequence_length:
            max_sequence_length = sequence_length
        self._self_setattr_tracking = False
        self._config_dict = {'vocab_size':vocab_size, 
         'embedding_width':embedding_width, 
         'hidden_size':hidden_size, 
         'num_layers':num_layers, 
         'num_attention_heads':num_attention_heads, 
         'sequence_length':sequence_length, 
         'max_sequence_length':max_sequence_length, 
         'type_vocab_size':type_vocab_size, 
         'intermediate_size':intermediate_size, 
         'activation':tf.keras.activations.serialize(activation), 
         'dropout_rate':dropout_rate, 
         'attention_dropout_rate':attention_dropout_rate, 
         'initializer':tf.keras.initializers.serialize(initializer)}
        word_ids = tf.keras.layers.Input(shape=(
         sequence_length,),
          dtype=(tf.int32),
          name='input_word_ids')
        mask = tf.keras.layers.Input(shape=(
         sequence_length,),
          dtype=(tf.int32),
          name='input_mask')
        type_ids = tf.keras.layers.Input(shape=(
         sequence_length,),
          dtype=(tf.int32),
          name='input_type_ids')
        self._embedding_layer = layers.OnDeviceEmbedding(vocab_size=vocab_size,
          embedding_width=embedding_width,
          initializer=initializer,
          name='word_embeddings')
        word_embeddings = self._embedding_layer(word_ids)
        self._position_embedding_layer = layers.PositionEmbedding(initializer=initializer,
          use_dynamic_slicing=True,
          max_sequence_length=max_sequence_length)
        position_embeddings = self._position_embedding_layer(word_embeddings)
        type_embeddings = layers.OnDeviceEmbedding(vocab_size=type_vocab_size,
          embedding_width=embedding_width,
          initializer=initializer,
          use_one_hot=True,
          name='type_embeddings')(type_ids)
        embeddings = tf.keras.layers.Add()([
         word_embeddings, position_embeddings, type_embeddings])
        embeddings = tf.keras.layers.LayerNormalization(name='embeddings/layer_norm',
          axis=(-1),
          epsilon=1e-12,
          dtype=(tf.float32))(embeddings)
        embeddings = tf.keras.layers.Dropout(rate=dropout_rate)(embeddings)
        if embedding_width != hidden_size:
            embeddings = layers.DenseEinsum(output_shape=hidden_size,
              kernel_initializer=initializer,
              name='embedding_projection')(embeddings)
        data = embeddings
        attention_mask = layers.SelfAttentionMask()([data, mask])
        shared_layer = layers.Transformer(num_attention_heads=num_attention_heads,
          intermediate_size=intermediate_size,
          intermediate_activation=activation,
          dropout_rate=dropout_rate,
          attention_dropout_rate=attention_dropout_rate,
          kernel_initializer=initializer,
          name='transformer')
        for _ in range(num_layers):
            data = shared_layer([data, attention_mask])

        first_token_tensor = tf.keras.layers.Lambda(lambda x: tf.squeeze((x[:, 0:1, :]), axis=1))(data)
        cls_output = tf.keras.layers.Dense(units=hidden_size,
          activation='tanh',
          kernel_initializer=initializer,
          name='pooler_transform')(first_token_tensor)
        (super(AlbertTransformerEncoder, self).__init__)(inputs=[
 word_ids, mask, type_ids], 
         outputs=[
 data, cls_output], **kwargs)

    def get_embedding_table(self):
        return self._embedding_layer.embeddings

    def get_config(self):
        return self._config_dict

    @classmethod
    def from_config(cls, config):
        return cls(**config)