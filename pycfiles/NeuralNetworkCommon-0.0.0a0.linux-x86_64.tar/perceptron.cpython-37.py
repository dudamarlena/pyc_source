# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/neuralnetworkcommon/perceptron.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 8781 bytes
from numpy import exp, array
import pythoncommontools.objectUtil.POPO as POPO
from random import random
from copy import copy

class Sigmoid:

    @staticmethod
    def value(variables):
        arrayVariables = array(variables)
        value = 1 / (1 + exp(-arrayVariables))
        return value

    @staticmethod
    def derivative(variables):
        arrayVariables = array(variables)
        derivative = variables * (1 - arrayVariables)
        return derivative


class TrainingDraft:

    def __init__(self, input, output):
        self.input = input
        self.output = output


class Layer(POPO):
    __doc__ = '\n    TODO : add extras parameters (uncertainties/dilatations/offsets)\n    all parameters should be randomized between some given ranges\n    TODO : parallelize random array generation\n    '

    @staticmethod
    def constructRandomFromDimensions(previousDimension, currentDimension):
        layer = Layer()
        layer.weights = [[(random() - 0.5) * 2 for _ in range(previousDimension)] for _ in range(currentDimension)]
        layer.biases = [
         0] * currentDimension
        return layer

    @staticmethod
    def constructFromAttributes(weights, biases):
        layer = Layer()
        layer.weights = weights
        layer.biases = biases
        return layer

    def instanciateNormalize(self):
        normalizedLayer = copy(self)
        normalizedLayer.biases = [float(_) for _ in self.biases]
        normalizedLayer.weights = list()
        for lineIndex, weightsLine in enumerate(self.weights):
            normalizedLine = [float(_) for _ in weightsLine]
            normalizedLayer.weights.append(normalizedLine)

        return normalizedLayer

    def passForward(self, input, training=False):
        weightsBiasInput = array(self.weights).dot(array(input)) + array(self.biases)
        output = Sigmoid.value(weightsBiasInput)
        if training:
            self.trainingDraft = TrainingDraft(input, output)
        return output

    def differentialErrorOutput(self, expectedOutput):
        differentialError = array(self.trainingDraft.output) - array(expectedOutput)
        return differentialError

    @staticmethod
    def differentialErrorHidden(previousDifferentielError, previousLayerWeights):
        differentialErrors = array(previousDifferentielError) * array(previousLayerWeights)
        differentialError = sum(differentialErrors, 0)
        return differentialError

    def computeNewWeights(self, differentialErrorLayer):
        differentialOutputWeightsBiasInput = Sigmoid.derivative(array([self.trainingDraft.output]))
        newDifferentialErrorWeightsBiases = (array(differentialErrorLayer) * differentialOutputWeightsBiasInput).T
        differentialErrorWeights = newDifferentialErrorWeightsBiases * array(self.trainingDraft.input)
        oldWeights = self.weights
        self.weights = oldWeights - 0.5 * differentialErrorWeights
        return (newDifferentialErrorWeightsBiases, oldWeights)

    def computeNewBiases(self, differentialErrorWeightsBiases):
        newBiases = array(self.biases) - 0.5 * array(differentialErrorWeightsBiases).T
        if len(newBiases.shape) == 2:
            if newBiases.shape[0] == 1:
                newBiases = newBiases[0]
        self.biases = newBiases

    def passBackward(self, expectedOutput=None, differentialErrorWeightsBiasInput=None, previousLayerWeights=None):
        if expectedOutput:
            differentialErrorLayer = self.differentialErrorOutput(expectedOutput)
        else:
            differentialErrorLayer = self.differentialErrorHidden(differentialErrorWeightsBiasInput, previousLayerWeights)
        newDifferentialErrorWeightsBiases, oldWeights = self.computeNewWeights(differentialErrorLayer)
        self.computeNewBiases(newDifferentialErrorWeightsBiases)
        del self.trainingDraft
        return (
         newDifferentialErrorWeightsBiases, oldWeights)


class Perceptron(POPO):

    @staticmethod
    def constructRandomFromDimensions(dimensions, workspaceId=None, comments=''):
        perceptron = Perceptron()
        perceptron.workspaceId = workspaceId
        perceptron.layers = [Layer.constructRandomFromDimensions(dimensions[index], dimensions[(index + 1)]) for index in range(len(dimensions) - 1)]
        perceptron.comments = comments
        return perceptron

    @staticmethod
    def constructFromAttributes(id, layers, workspaceId=None, comments=''):
        perceptron = Perceptron()
        perceptron.id = id
        perceptron.workspaceId = workspaceId
        perceptron.layers = layers
        perceptron.comments = comments
        return perceptron

    def passForward(self, input, training=False):
        inputOutput = input
        for layer in self.layers:
            inputOutput = layer.passForward(inputOutput, training)

        return inputOutput

    def passBackward(self, expectedOutput):
        layer = self.layers[(-1)]
        differentialErrorWeightsBiasInput, previousLayerWeights = layer.passBackward(expectedOutput=expectedOutput)
        for hiddenLayerIndex in range(2, len(self.layers) + 1):
            layer = self.layers[(-hiddenLayerIndex)]
            differentialErrorWeightsBiasInput, previousLayerWeights = layer.passBackward(differentialErrorWeightsBiasInput=differentialErrorWeightsBiasInput, previousLayerWeights=previousLayerWeights)

    def passForwardBackward(self, input, expectedOutput):
        actualOutput = self.passForward(array(input), True)
        outputError = (array(expectedOutput) - array(actualOutput)) ** 2 / 2
        totalError = sum(outputError)
        self.passBackward(expectedOutput)
        return totalError


class LayerSummary:

    @staticmethod
    def constructFromAttributes(weightsDimensions, biasesDimension):
        layerSummary = LayerSummary()
        layerSummary.weightsDimensions = weightsDimensions
        layerSummary.biasesDimension = biasesDimension
        return layerSummary


class PerceptronSummary(POPO):

    @staticmethod
    def constructFromAttributes(workspaceId, layersSummary, comments=''):
        perceptronSummary = PerceptronSummary()
        perceptronSummary.workspaceId = workspaceId
        perceptronSummary.layersSummary = layersSummary
        perceptronSummary.comments = comments
        return perceptronSummary