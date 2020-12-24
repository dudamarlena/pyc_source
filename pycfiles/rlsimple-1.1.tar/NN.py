# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/liup/RL/rlsimpleParent/rlsimple/NN.py
# Compiled at: 2017-04-09 21:59:13
import tensorflow as tf, sys

class NN:

    def __init__(self, session, hasShadowNet=True):
        self._session = session
        if hasShadowNet == True:
            self._ema = tf.train.ExponentialMovingAverage(0.999)
        else:
            self._ema = None
        self._weight_counter = 0
        self._bias_counter = 0
        self._layer_counter = 0
        self._operation_counter = 0
        self._anyNamedOperations = {}
        self._layers = {}
        self._variables = {}
        self._placeholders = {}
        self._layers2shadow = {}
        self._variables2shadow = {}
        self._placeholders2shadow = {}
        self._flushShadowNetOps = []
        self._graphviz = ''
        return

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.01)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)

    def uniqueWeightName(self):
        self._weight_counter += 1
        return 'W' + str(self._weight_counter)

    def uniqueBiasName(self):
        self._bias_counter += 1
        return 'B' + str(self._bias_counter)

    def uniqueLayerName(self):
        self._layer_counter += 1
        return 'L' + str(self._layer_counter)

    def shape2string(self, weightShape):
        string = ''
        index = 0
        for i in weightShape:
            dimString = str(i)
            if dimString == '?':
                string += 'UNK'
            else:
                string += dimString
            if index != len(weightShape) - 1:
                string += '*'
            index += 1

        return string

    def shadowPrefixed(self, x):
        return 'Shadow' + x

    def buildInputLayer(self, name, shape):
        holder = tf.placeholder('float', shape=shape)
        self._layers[name] = holder
        self._placeholders[name] = holder
        self._layers2shadow[holder] = holder
        self._placeholders2shadow[holder] = holder
        return holder

    def buildLinearReluWire(self, layer, weightShape):
        W1 = self.weight_variable(shape=weightShape)
        B1 = self.bias_variable(shape=[weightShape[(-1)]])
        tmp = tf.matmul(layer, W1) + B1
        outputLayer = tf.nn.relu(tmp)
        weightName = self.uniqueWeightName()
        self._variables[weightName] = W1
        biasName = self.uniqueBiasName()
        self._variables[biasName] = B1
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = weightName + ':' + self.shape2string(weightShape) + ',' + biasName + ':' + self.shape2string([weightShape[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            flush = self._ema.apply([W1, B1])
            self._flushShadowNetOps.append(flush)
            W1shadow = self._ema.average(W1)
            B1shadow = self._ema.average(B1)
            layerShadow = self._layers2shadow[layer]
            tmpshadow = tf.matmul(layerShadow, W1shadow) + B1shadow
            outputLayershadow = tf.nn.relu(tmpshadow)
            self._variables2shadow[W1] = W1shadow
            self._variables2shadow[B1] = B1shadow
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer

    def buildJointLinearReluWire(self, layer, weightShape, layer2, weightShape2):
        W1 = self.weight_variable(shape=weightShape)
        B = self.bias_variable(shape=[weightShape[(-1)]])
        W2 = self.weight_variable(shape=weightShape2)
        if weightShape[(-1)] != weightShape2[(-1)]:
            print 'they should agree!'
            sys.exit(1)
        tmp = tf.matmul(layer, W1) + tf.matmul(layer2, W2) + B
        outputLayer = tf.nn.relu(tmp)
        weightName = self.uniqueWeightName()
        self._variables[weightName] = W1
        weightName2 = self.uniqueWeightName()
        self._variables[weightName2] = W2
        biasName = self.uniqueBiasName()
        self._variables[biasName] = B
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = weightName + ':' + self.shape2string(weightShape) + ',' + biasName + ':' + self.shape2string([weightShape[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        label2 = weightName2 + ':' + self.shape2string(weightShape2) + ',' + biasName + ':' + self.shape2string([weightShape2[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer2), layerName, label2)
        if self._ema != None:
            flush = self._ema.apply([W1, W2, B])
            self._flushShadowNetOps.append(flush)
            W1shadow = self._ema.average(W1)
            W2shadow = self._ema.average(W2)
            Bshadow = self._ema.average(B)
            layerShadow = self._layers2shadow[layer]
            layer2Shadow = self._layers2shadow[layer2]
            tmpshadow = tf.matmul(layerShadow, W1shadow) + tf.matmul(layer2Shadow, W2shadow) + Bshadow
            outputLayershadow = tf.nn.relu(tmpshadow)
            self._variables2shadow[W1] = W1shadow
            self._variables2shadow[B] = Bshadow
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer2)), self.shadowPrefixed(layerName), label2)
        return outputLayer

    def buildLinearWire(self, layer, weightShape):
        W1 = self.weight_variable(shape=weightShape)
        B1 = self.bias_variable(shape=[weightShape[(-1)]])
        outputLayer = tf.matmul(layer, W1) + B1
        weightName = self.uniqueWeightName()
        self._variables[weightName] = W1
        biasName = self.uniqueBiasName()
        self._variables[biasName] = B1
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        label = weightName + ':' + self.shape2string(weightShape) + ',' + biasName + ':' + self.shape2string([weightShape[(-1)]])
        self.createGraphvizEdge(self.lookupLayerName(layer), layerName, label)
        if self._ema != None:
            flush = self._ema.apply([W1, B1])
            self._flushShadowNetOps.append(flush)
            W1shadow = self._ema.average(W1)
            B1shadow = self._ema.average(B1)
            layerShadow = self._layers2shadow[layer]
            outputLayershadow = tf.matmul(layerShadow, W1shadow) + B1shadow
            self._variables2shadow[W1] = W1shadow
            self._variables2shadow[B1] = B1shadow
            self._layers2shadow[outputLayer] = outputLayershadow
            self.createGraphvizEdge(self.shadowPrefixed(self.lookupLayerName(layer)), self.shadowPrefixed(layerName), label)
        return outputLayer

    def buildReduceSum(self, layer, reduction_indices):
        outputLayer = tf.reduce_sum(layer, reduction_indices=reduction_indices)
        layerName = self.uniqueLayerName()
        self._layers[layerName] = outputLayer
        if self._ema != None:
            layerShadow = self._layers2shadow[layer]
            outputLayerShadow = tf.reduce_sum(layerShadow, reduction_indices=reduction_indices)
            self._layers2shadow[outputLayer] = outputLayerShadow
        return outputLayer

    def addDescentOperation(self, extraGradients):
        varList = self._variables.values()
        gradient = tf.gradients(self._out, varList, extraGradients)
        zipped = zip(gradient, varList)
        descent = tf.train.AdamOptimizer(1e-06).apply_gradients(zipped)
        self._descentOp = descent
        return descent

    def addAscentOperation(self, extraGradients):
        varList = self._variables.values()
        gradient = tf.gradients(self._out, varList, extraGradients)

        def multbyNegativeOne(elem):
            return elem * -1

        negativegradient = map(multbyNegativeOne, gradient)
        zipped = zip(negativegradient, varList)
        ascent = tf.train.AdamOptimizer(1e-06).apply_gradients(zipped)
        self._ascentOp = ascent
        return ascent

    def addMinimizeOperation(self, minimizer):
        self._minimize = minimizer

    def addAnyNamedOperation(self, name, op):
        self._anyNamedOperations[name] = op

    def setOutLayer(self, out):
        self._out = out
        if self._ema != None:
            self._shadowOut = self._layers2shadow[out]
        return

    def getInputLayer(self, name):
        return self._layers[name]

    def lookupLayerName(self, layer):
        for key, value in self._layers.iteritems():
            if value == layer:
                return key

    def createGraphvizEdge(self, name1, name2, label):
        self._graphviz += name1
        self._graphviz += ' -> '
        self._graphviz += name2
        self._graphviz += ' [label="'
        self._graphviz += label
        self._graphviz += '"]\n'

    def visualizeGraphviz(self):
        for layerName, value in self._layers.iteritems():
            if value != self._out and value not in self._placeholders.values():
                self._graphviz = layerName + '\n' + self._graphviz
                self._graphviz = self.shadowPrefixed(layerName) + '\n' + self._graphviz
            elif value == self._out:
                self._graphviz = layerName + ' [label=Out]\n' + self._graphviz
                self._graphviz = self.shadowPrefixed(layerName) + ' [label=ShadowOut]\n' + self._graphviz
            elif value in self._placeholders.values():
                self._graphviz = layerName + ' [label="' + layerName + ':' + self.shape2string(value.get_shape()) + '"]\n' + self._graphviz
                self._graphviz = self.shadowPrefixed(layerName) + ' [label="' + self.shadowPrefixed(layerName) + ':' + self.shape2string(value.get_shape()) + '"]\n' + self._graphviz

        self._graphviz = 'digraph G{\n                            edge [dir=forward]\n                            node [shape=plaintext]\n                            ' + self._graphviz + '\n                            }'
        from graphviz import Source
        s = Source(self._graphviz, filename='test.gv', format='png')
        s.view()

    def descentSmartly(self, feed_dict_string_key):
        if self._descentOp == None:
            print 'add descent operation first!!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        self._session.run(self._descentOp, feed_dict=feed_dict)
        for flush in self._flushShadowNetOps:
            self._session.run(flush)

        return

    def ascentSmartly(self, feed_dict_string_key):
        if self._ascentOp == None:
            print 'add ascent operation first!!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        self._session.run(self._ascentOp, feed_dict=feed_dict)
        for flush in self._flushShadowNetOps:
            self._session.run(flush)

        return

    def minimizeSmartly(self, feed_dict_string_key):
        if self._minimize == None:
            print 'set self._minimize operation first!!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        self._session.run(self._minimize, feed_dict=feed_dict)
        for flush in self._flushShadowNetOps:
            self._session.run(flush)

        return

    def anyNamedOperation(self, name, feed_dict_string_key, isUpdate):
        if self._anyNamedOperations[name] == None:
            print 'set the anyoperation you named !!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        ret = self._session.run(self._anyNamedOperations[name], feed_dict=feed_dict)
        if isUpdate:
            for flush in self._flushShadowNetOps:
                self._session.run(flush)

        return ret

    def getOutValueSmartly(self, feed_dict_string_key):
        if self._ema == None:
            return self.__getOutValue__(feed_dict_string_key)
        else:
            return self.__getShadownOutValue__(feed_dict_string_key)
            return

    def __getShadownOutValue__(self, feed_dict_string_key):
        if self._shadowOut == None:
            print 'set out layer first!!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        return self._session.run(self._shadowOut, feed_dict=feed_dict)

    def __getOutValue__(self, feed_dict_string_key):
        if self._out == None:
            print 'set out layer first!!!'
            sys.exit(1)
        feed_dict = {}
        for key, value in feed_dict_string_key.iteritems():
            feed_dict[self._placeholders[key]] = value

        return self._session.run(self._out, feed_dict=feed_dict)