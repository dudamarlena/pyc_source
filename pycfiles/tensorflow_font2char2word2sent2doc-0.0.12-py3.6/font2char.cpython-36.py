# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/font2char.py
# Compiled at: 2017-04-14 04:25:54
# Size of source mod 2**32: 1638 bytes
import extenteten as ex, extenteten.collections as collections, tensorflow as tf

@ex.func_scope()
def font2char(font, *, nums_of_channels, nums_of_attention_channels):
    assert ex.static_rank(font) == 3
    h = tf.contrib.slim.flatten(_cnn(_attend_to_image(tf.expand_dims(font, -1), nums_of_attention_channels), nums_of_channels))
    ex.summary.image(tf.expand_dims(tf.expand_dims(h[:256], 0), 3))
    return h


@ex.func_scope()
def _attend_to_image(images, nums_of_channels):
    assert ex.static_rank(images) == 4
    attentions = _calculate_attention(images, nums_of_channels)
    collections.add_attention(attentions)
    return tf.transpose(tf.transpose(images) * tf.transpose(attentions))


@ex.func_scope()
def _calculate_attention(images, nums_of_channels):
    assert ex.static_rank(images) == 4
    logits = tf.squeeze((tf.image.resize_nearest_neighbor(tf.expand_dims(tf.reduce_sum((_cnn(images, nums_of_channels)), axis=3),
      axis=(-1)), tf.shape(images)[1:3])),
      axis=3)
    return tf.reshape(tf.nn.softmax(tf.reshape(logits, [tf.shape(logits)[0], -1])), tf.shape(logits))


@ex.func_scope()
def _cnn(h, nums_of_channels):
    assert ex.static_rank(h) == 4
    for index, num_of_channels in enumerate(nums_of_channels):
        h = tf.contrib.slim.conv2d(h,
          num_of_channels, 3, scope=('conv{}'.format(index)))
        h = tf.contrib.slim.max_pool2d(h, 2, 2, scope=('pool{}'.format(index)))

    return h