# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/liup/RL/rlsimpleParent/rlsimple/CNN.py
# Compiled at: 2017-04-09 22:27:13
from NN import NN
import tensorflow as tf

class CNN(NN):

    def __init__(self, session, hasShadowNet=True):
        NN.__init__(self, session, hasShadowNet)

    def conv2d(self, x, filterWindow, strides):
        return tf.nn.conv2d(x, filterWindow, strides=strides, padding='SAME')

    def max_pool(self, x, filterWindow, strides):
        return tf.nn.max_pool(x, ksize=filterWindow, strides=strides, padding='SAME')

    def buildConvReluWire(self, layer, filterWindow, strides):
        W1 = self.weight_variable(shape=filterWindow)
        B1 = self.bias_variable(shape=[filterWindow[(-1)]])
        tmp = tf.nn.bias_add(self.conv2d(layer, W1, strides), B1)
        outputLayer = tf.nn.relu(tmp)
        weightName = self.uniqueWeightName()
        self._variables[weightName] = W1
        biasName = self.uniqueBiasName()
        self._variables[biasName] = B1
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = weightName + ':' + self.shape2string(filterWindow) + ',' + biasName + ':' + self.shape2string([filterWindow[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            flush = self._ema.apply([W1, B1])
            self._flushShadowNetOps.append(flush)
            W1shadow = self._ema.average(W1)
            B1shadow = self._ema.average(B1)
            layerShadow = self._layers2shadow[layer]
            tmpshadow = tf.nn.bias_add(self.conv2d(layerShadow, W1shadow, strides), B1shadow)
            outputLayershadow = tf.nn.relu(tmpshadow)
            self._variables2shadow[W1] = W1shadow
            self._variables2shadow[B1] = B1shadow
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer

    def buildConvWire(self, layer, filterWindow, strides):
        W1 = self.weight_variable(shape=filterWindow)
        B1 = self.bias_variable(shape=[filterWindow[(-1)]])
        outputLayer = tf.nn.bias_add(self.conv2d(layer, W1, strides), B1)
        weightName = self.uniqueWeightName()
        self._variables[weightName] = W1
        biasName = self.uniqueBiasName()
        self._variables[biasName] = B1
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = weightName + ':' + self.shape2string(filterWindow) + ',' + biasName + ':' + self.shape2string([filterWindow[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            flush = self._ema.apply([W1, B1])
            self._flushShadowNetOps.append(flush)
            W1shadow = self._ema.average(W1)
            B1shadow = self._ema.average(B1)
            layerShadow = self._layers2shadow[layer]
            outputLayershadow = tf.nn.bias_add(self.conv2d(layerShadow, W1shadow, strides), B1shadow)
            self._variables2shadow[W1] = W1shadow
            self._variables2shadow[B1] = B1shadow
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer

    def buildMaxpoolWire(self, layer, filterWindow=[
 1, 2, 2, 1], strides=[1, 2, 2, 1]):
        outputLayer = self.max_pool(layer, filterWindow, strides)
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = 'maxpool2*2'
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            layerShadow = self._layers2shadow[layer]
            outputLayershadow = self.max_pool(layerShadow, filterWindow, strides)
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer

    def buildFlattenWire(self, layer, flattenAs):
        outputLayer = tf.reshape(layer, flattenAs)
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = 'flattenAs' + self.shape2string(flattenAs)
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            layerShadow = self._layers2shadow[layer]
            outputLayershadow = tf.reshape(layerShadow, flattenAs)
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer