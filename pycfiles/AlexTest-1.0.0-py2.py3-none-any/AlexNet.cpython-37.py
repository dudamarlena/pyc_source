# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\source\AlexNet.py
# Compiled at: 2019-10-03 05:29:54
# Size of source mod 2**32: 6132 bytes
__doc__ = '\nCreated on Tue Sep 10 17:03:56 2019\n\n@author: Administrator\n'
import tensorflow as tf, numpy as np

def maxPoolLayer(x, kHeight, kWidth, strideX, strideY, name, padding='SAME'):
    """max-pooling"""
    return tf.nn.max_pool(x, ksize=[1, kHeight, kWidth, 1], strides=[
     1, strideX, strideY, 1],
      padding=padding,
      name=name)


def dropout(x, keepPro, name=None):
    """dropout"""
    return tf.nn.dropout(x, keepPro, name)


def LRN(x, R, alpha, beta, name=None, bias=1.0):
    """LRN"""
    return tf.nn.local_response_normalization(x, depth_radius=R, alpha=alpha, beta=beta,
      bias=bias,
      name=name)


def fcLayer(x, inputD, outputD, reluFlag, name):
    """fully-connect"""
    with tf.variable_scope(name) as (scope):
        w = tf.get_variable('w', shape=[inputD, outputD], dtype='float')
        b = tf.get_variable('b', [outputD], dtype='float')
        out = tf.nn.xw_plus_b(x, w, b, name=(scope.name))
        if reluFlag:
            return tf.nn.relu(out)
        return out


def fc_layers_1(x, classNum, batch_size):
    with tf.variable_scope('fc_1') as (scope):
        reshape = tf.reshape(x, shape=[batch_size, -1])
        dim = reshape.get_shape()[1].value
        local3_weights = tf.get_variable('local3_weights_name', shape=[
         dim, 448],
          dtype=(tf.float32),
          initializer=tf.truncated_normal_initializer(stddev=0.01, dtype=(tf.float32)))
        biases = tf.get_variable('biases', shape=[
         448],
          dtype=(tf.float32),
          initializer=(tf.constant_initializer(0.1)))
        local3 = tf.nn.relu((tf.matmul(reshape, local3_weights) + biases), name=(scope.name))
        return local3


def fc_layers(x, classNum, reluFlag):
    with tf.variable_scope('softmax_linear') as (scope):
        dim = x.get_shape().as_list()[(-1)]
        softmax_weights = tf.get_variable('softmax_linear', shape=[
         dim, classNum],
          dtype=(tf.float32),
          initializer=tf.truncated_normal_initializer(stddev=0.01, dtype=(tf.float32)))
        softmax_biases = tf.get_variable('biases', shape=[
         classNum],
          dtype=(tf.float32),
          initializer=(tf.constant_initializer(0.1)))
        softmax_linear = tf.add((tf.matmul(x, softmax_weights)), softmax_biases,
          name='softmax_linear')
        if reluFlag:
            return tf.nn.relu(softmax_linear)
        return softmax_linear


def convLayer(x, kHeight, kWidth, strideX, strideY, featureNum, name, padding='SAME', groups=1):
    """convolution"""
    channel = int(x.get_shape()[(-1)])
    conv = lambda a, b: tf.nn.conv2d(a, b, strides=[1, strideY, strideX, 1], padding=padding)
    with tf.variable_scope(name) as (scope):
        w = tf.get_variable('w', shape=[kHeight, kWidth, channel / groups, featureNum])
        b = tf.get_variable('b', shape=[featureNum])
        xNew = tf.split(value=x, num_or_size_splits=groups, axis=3)
        wNew = tf.split(value=w, num_or_size_splits=groups, axis=3)
        featureMap = [conv(t1, t2) for t1, t2 in zip(xNew, wNew)]
        mergeFeatureMap = tf.concat(axis=3, values=featureMap)
        out = tf.nn.bias_add(mergeFeatureMap, b)
        return tf.nn.relu((tf.reshape(out, mergeFeatureMap.get_shape().as_list())), name=(scope.name))


class alexNet(object):
    """alexNet"""

    def __init__(self, x, keepPro, classNum, batch_size):
        self.X = x
        self.KEEPPRO = keepPro
        self.CLASSNUM = classNum
        self.BATCH_SIZE = batch_size
        self.buildCNN()

    def buildCNN(self):
        """build model"""
        conv1 = convLayer(self.X, 11, 11, 4, 4, 96, 'conv1', 'VALID')
        lrn1 = LRN(conv1, 2, 2e-05, 0.75, 'norm1')
        pool1 = maxPoolLayer(lrn1, 3, 3, 2, 2, 'pool1', 'VALID')
        conv2 = convLayer(pool1, 5, 5, 1, 1, 256, 'conv2', groups=2)
        lrn2 = LRN(conv2, 2, 2e-05, 0.75, 'lrn2')
        pool2 = maxPoolLayer(lrn2, 3, 3, 2, 2, 'pool2', 'VALID')
        conv3 = convLayer(pool2, 3, 3, 1, 1, 384, 'conv3')
        conv4 = convLayer(conv3, 3, 3, 1, 1, 384, 'conv4', groups=2)
        conv5 = convLayer(conv4, 3, 3, 1, 1, 256, 'conv5', groups=2)
        pool5 = maxPoolLayer(conv5, 3, 3, 2, 2, 'pool5', 'VALID')
        fcIn = tf.reshape(pool5, [-1, 9216])
        fc1 = fcLayer(fcIn, 9216, 4096, True, 'fc6')
        dropout1 = dropout(fc1, self.KEEPPRO)
        fc2 = fc_layers_1(dropout1, self.CLASSNUM, self.BATCH_SIZE)
        dropout2 = dropout(fc2, self.KEEPPRO)
        self.fc3 = fc_layers(dropout2, self.CLASSNUM, True)