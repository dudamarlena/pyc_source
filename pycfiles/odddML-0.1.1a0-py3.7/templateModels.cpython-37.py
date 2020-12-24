# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\odddML\templateModels.py
# Compiled at: 2019-12-20 04:25:29
# Size of source mod 2**32: 1601 bytes
from tensorflow.keras import models
from tensorflow.keras import layers
from odddML.custom_layers import *
import tensorflow as tf
from odddML.utils import *
import numpy as np, os

class SimpleConv2DClassifier(tf.keras.Model):
    __doc__ = '\n    # Arguments\n        image_shape: tuple shape of each image, check it out with im.shape() should be (samples, x, y, channels) you input (x,y,channels)\n        num_classes: number of classes of your problem\n    #### Usage: Use it as a keras model, just compile it with categorical_crossentropy and fit it on the data.  \n    '

    def __init__(self, num_classes):
        super(SimpleConv2DClassifier, self).__init__()
        self.conv_inp = tf.keras.layers.Conv2D(32, (3, 3), activation='relu')
        self.conv_64 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu')
        self.maxP = tf.keras.layers.MaxPooling2D((2, 2))
        self.conv_32 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu')
        self.flat = tf.keras.layers.Flatten()
        self.FC_l1 = tf.keras.layers.Dense(120, activation='relu')
        self.FC_l2 = tf.keras.layers.Dense(10, activation='relu')
        self.classifier = tf.keras.layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        x = self.conv_inp(inputs)
        x = self.maxP(x)
        x = self.conv_64(x)
        x = self.maxP(x)
        x = self.conv_32(x)
        x = self.flat(x)
        x = self.FC_l1(x)
        x = self.FC_l2(x)
        x = self.classifier(x)
        return x


if __name__ == '__main__':
    pass