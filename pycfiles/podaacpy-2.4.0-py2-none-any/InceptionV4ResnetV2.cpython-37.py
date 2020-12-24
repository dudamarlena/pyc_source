# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\poda\segmentation\InceptionV4ResnetV2.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 18039 bytes
import tensorflow as tf
from poda.layers.convolutional import *

class InceptionV4ResnetV2(object):

    def __init__(self, is_training=True):
        """[summary]
        
        Arguments:
            num_classes {[type]} -- [description]
        
        Keyword Arguments:
            input_tensor {[type]} -- [description] (default: {None})
            input_shape {tuple} -- [description] (default: {(None, 300, 300, 3)})
            learning_rate {float} -- [description] (default: {0.0001})
            is_training {bool} -- [description] (default: {True})
        """
        self.is_training = is_training

    def conv_block(self, inputs, filters, kernel_size, strides=(2, 2), padding='VALID', dropout_rate=0.2, activation='relu', batch_normalization=True):
        """[summary]
        
        Arguments:
            inputs {[type]} -- [description]
            filters {[type]} -- [description]
            kernel_size {[type]} -- [description]
        
        Keyword Arguments:
            strides {tuple} -- [description] (default: {(2,2)})
            padding {str} -- [description] (default: {'valid'})
            batch_normalization {bool} -- [description] (default: {True})
            dropout_rate {float} -- [description] (default: {0.15})
            activation {str} -- [description] (default: {'relu'})
            is_training {bool} -- [description] (default: {True})
        
        Returns:
            [type] -- [description]
        """
        conv = convolution_2d(input_tensor=inputs, number_filters=filters, kernel_sizes=kernel_size, stride_sizes=strides,
          paddings=padding,
          activations=activation)
        conv = batch_normalization(input_tensor=conv, is_trainable=batch_normalization)
        conv = dropout(input_tensor=conv, dropout_rates=dropout_rate)
        return conv

    def stem_block(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        conv_1 = self.conv_block(inputs=input_tensor, filters=32, kernel_size=(3, 3), strides=(2,
                                                                                               2), batch_normalization=batch_normalization)
        conv_2 = self.conv_block(inputs=conv_1, filters=32, kernel_size=(3, 3), strides=(1,
                                                                                         1), batch_normalization=batch_normalization)
        conv_3 = self.conv_block(inputs=conv_2, filters=64, kernel_size=(3, 3), padding='same', strides=(1,
                                                                                                         1), batch_normalization=batch_normalization)
        conv_4 = self.conv_block(inputs=conv_3, filters=96, kernel_size=(3, 3), strides=(2,
                                                                                         2), batch_normalization=batch_normalization)
        max_pool_1 = max_pool_2d(input_tensor=conv_3, pool_sizes=(3, 3), stride_sizes=(2,
                                                                                       2))
        concat_1 = tf.concat([conv_4, max_pool_1], -1)
        conv_5 = self.conv_block(inputs=concat_1, filters=64, kernel_size=(3, 3), strides=(1,
                                                                                           1), batch_normalization=batch_normalization)
        conv_6 = self.conv_block(inputs=conv_5, filters=64, kernel_size=(7, 1), padding='same', strides=(1,
                                                                                                         1), batch_normalization=batch_normalization)
        conv_7 = self.conv_block(inputs=conv_6, filters=64, kernel_size=(1, 7), padding='same', strides=(1,
                                                                                                         1), batch_normalization=batch_normalization)
        conv_8 = self.conv_block(inputs=conv_7, filters=96, kernel_size=(3, 3), padding='same', strides=(1,
                                                                                                         1), batch_normalization=batch_normalization)
        conv_9 = self.conv_block(inputs=concat_1, filters=64, kernel_size=(1, 1), strides=(1,
                                                                                           1), batch_normalization=batch_normalization)
        conv_10 = self.conv_block(inputs=conv_9, filters=96, kernel_size=(3, 3), strides=(1,
                                                                                          1), batch_normalization=batch_normalization)
        concat_2 = tf.concat([conv_8, conv_10], -1)
        max_pool_2 = max_pool_2d(inputs=concat_2, pool_sizes=(3, 3), stride_sizes=(2,
                                                                                   2))
        conv_11 = self.conv_block(inputs=concat_2, filters=192, kernel_size=(3, 3), strides=(2,
                                                                                             2), batch_normalization=batch_normalization)
        concat_3 = tf.concat([max_pool_2, conv_11], -1)
        return concat_3

    def inception_resnet_a(self, input_tensor, drop_out=0.8, batch_normalization=True):
        """[summary]
        
        Arguments:
            inputs {[type]} -- [description]
        
        Keyword Arguments:
            drop_out {float} -- [description] (default: {0.85})
            activation {str} -- [description] (default: {'NONE'})
            is_training {bool} -- [description] (default: {True})
            use_bias {bool} -- [description] (default: {True})
            use_batchnorm {bool} -- [description] (default: {True})
        """
        conv_1 = self.conv_block(inputs=input_tensor, filters=64, kernel_size=(1, 1), strides=(1,
                                                                                               1), batch_normalization=batch_normalization)
        conv_2 = self.conv_block(inputs=conv_1, filters=96, kernel_size=(3, 3), strides=(1,
                                                                                         1), batch_normalization=batch_normalization)
        conv_3 = self.conv_block(inputs=conv_2, filters=96, kernel_size=(3, 3), strides=(1,
                                                                                         1), batch_normalization=batch_normalization)
        conv_4 = self.conv_block(inputs=input_tensor, filters=64, kernel_size=(1, 1), strides=(1,
                                                                                               1), batch_normalization=batch_normalization)
        conv_5 = self.conv_block(inputs=conv_4, filters=96, kernel_size=(3, 3), strides=(1,
                                                                                         1), batch_normalization=batch_normalization)
        conv_6 = self.conv_block(inputs=input_tensor, filters=96, kernel_size=(1, 1), strides=(1,
                                                                                               1), batch_normalization=batch_normalization)
        conv_7 = self.conv_block(inputs=conv_2, filters=96, kernel_size=(3, 3), strides=(1,
                                                                                         1), batch_normalization=batch_normalization)
        input_depth = conv_right1.get_shape().as_list()[(-1)]
        conv_right2, _ = new_conv2d_layer(input=conv_right1, filter_shape=[
         3, 3, input_depth, 48],
          name='inres_a_conv_r2',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_right2.get_shape().as_list()[(-1)]
        conv_right3, _ = new_conv2d_layer(input=conv_right2, filter_shape=[
         3, 3, input_depth, 32],
          name='inres_a_conv_r3',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_mid1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         1, 1, input_depth, 32],
          name='inres_a_conv_m1',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_mid1.get_shape().as_list()[(-1)]
        conv_mid2, _ = new_conv2d_layer(input=conv_mid1, filter_shape=[
         3, 3, input_depth, 32],
          name='inres_a_conv_m2',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_left1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         1, 1, input_depth, 32],
          name='inres_a_conv_l1',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        concat_conv = tf.concat([conv_right3, conv_mid2, conv_left1], -1)
        input_depth = concat_conv.get_shape().as_list()[(-1)]
        output_depth = inputs.get_shape().as_list()[(-1)]
        conv_mixed, _ = new_conv2d_layer(input=concat_conv, filter_shape=[
         1, 1, input_depth, output_depth],
          name='inres_a_conv_concat',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        final_conv = inputs + conv_mixed
        return final_conv

    def reduction_a(self, inputs, drop_out=0.8, activation='NONE', use_bias=True, use_batchnorm=True):
        """[summary]
        
        Arguments:
            inputs {[type]} -- [description]
        
        Keyword Arguments:
            drop_out {float} -- [description] (default: {0.85})
            activation {str} -- [description] (default: {'NONE'})
            is_training {bool} -- [description] (default: {True})
            use_bias {bool} -- [description] (default: {True})
            use_batchnorm {bool} -- [description] (default: {True})
        """
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_right1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         1, 1, input_depth, 256],
          name='reduc_a_conv_r1',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_right1.get_shape().as_list()[(-1)]
        conv_right2, _ = new_conv2d_layer(input=conv_right1, filter_shape=[
         3, 3, input_depth, 256],
          name='reduc_a_conv_r2',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_right2.get_shape().as_list()[(-1)]
        conv_right3, _ = new_conv2d_layer(input=conv_right2, filter_shape=[
         3, 3, input_depth, 384],
          name='reduc_a_conv_r3',
          dropout_val=drop_out,
          activation=activation,
          strides=[
         1, 2, 2, 1],
          padding='VALID',
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_mid1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         3, 3, input_depth, 384],
          name='reduc_a_conv_m1',
          dropout_val=drop_out,
          activation=activation,
          strides=[
         1, 2, 2, 1],
          padding='VALID',
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        return tf.concat([conv_right3, conv_mid1], (-1), name='hellloooooo')

    def inception_resnet_b(self, inputs, drop_out=0.8, activation='NONE', use_bias=True, use_batchnorm=True):
        """[summary]
        
        Arguments:
            inputs {[type]} -- [description]
        
        Keyword Arguments:
            drop_out {float} -- [description] (default: {0.85})
            activation {str} -- [description] (default: {'NONE'})
            is_training {bool} -- [description] (default: {True})
            use_bias {bool} -- [description] (default: {True})
            use_batchnorm {bool} -- [description] (default: {True})
        """
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_right1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         1, 1, input_depth, 128],
          name='inres_a_conv_r1',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_right1.get_shape().as_list()[(-1)]
        conv_right2, _ = new_conv2d_layer(input=conv_right1, filter_shape=[
         1, 7, input_depth, 160],
          name='inres_a_conv_r2',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = conv_right2.get_shape().as_list()[(-1)]
        conv_right3, _ = new_conv2d_layer(input=conv_right2, filter_shape=[
         7, 1, input_depth, 192],
          name='inres_a_conv_r3',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        input_depth = inputs.get_shape().as_list()[(-1)]
        conv_mid1, _ = new_conv2d_layer(input=inputs, filter_shape=[
         1, 1, input_depth, 192],
          name='inres_a_conv_m1',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        concat_conv = tf.concat([conv_right3, conv_mid1], -1)
        input_depth = concat_conv.get_shape().as_list()[(-1)]
        output_depth = inputs.get_shape().as_list()[(-1)]
        conv_mixed, _ = new_conv2d_layer(input=concat_conv, filter_shape=[
         1, 1, input_depth, output_depth],
          name='inres_a_conv_mx',
          dropout_val=drop_out,
          activation=activation,
          is_training=(self.is_training),
          use_bias=use_bias,
          use_batchnorm=use_batchnorm)
        final_conv = inputs + conv_mixed
        return final_conv

    def create_base_model(self, input=None):
        """[summary]
        
        Arguments:
            classes {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        with tf.variable_scope('stem'):
            net = self.stem_block(input)
        print(net, '===================>>>')
        with tf.variable_scope('inception_resnet_a'):
            for i in range(5):
                net = self.inception_resnet_a(inputs=net)

        print(net, '===================>>>')
        with tf.variable_scope('reduction_a'):
            net = self.reduction_a(inputs=net)
        print(net, '===================>>>')
        with tf.variable_scope('inception_resnet_b'):
            for i in range(10):
                net = self.inception_resnet_b(inputs=net)

        print(net, '===================>>>')
        return net