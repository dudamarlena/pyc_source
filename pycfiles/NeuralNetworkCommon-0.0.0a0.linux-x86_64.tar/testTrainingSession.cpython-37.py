# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/test/testTrainingSession.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 2067 bytes
from unittest import TestCase
from random import randint, random
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkcommon.trainingElement import TrainingElement
from neuralnetworkcommon.trainingSet import TrainingSet
from neuralnetworkcommon.trainingSession import TrainingSession

class testTrainingSession(TestCase):

    def testConstructFromTrainingSet(self):
        layersNumber = randint(2, 12)
        dimensions = [randint(2, 100) for _ in range(layersNumber)]
        perceptron = Perceptron.constructRandomFromDimensions(dimensions)
        trainingElements = list()
        trainingSize = randint(15, 95)
        inputDimension = randint(20, 100)
        outputDimension = randint(20, 100)
        for _ in range(trainingSize):
            input = [(random() - 0.5) * 2 for _ in range(inputDimension)]
            expectedOutput = [(random() - 0.5) * 2 for _ in range(outputDimension)]
            trainingElement = TrainingElement.constructFromAttributes(input, expectedOutput)
            trainingElements.append(trainingElement)

        trainingSet = TrainingSet.constructFromAttributes(None, trainingElements)
        expectedDataSet = set(trainingSet.trainingElements)
        trainingSession = TrainingSession.constructFromTrainingSet(perceptron, trainingSet, randint(2, 10), randint(100, 200), randint(1, 10), randint(1, 10), random(), random())
        actualTrainingSet = set(trainingSession.trainingSet)
        actualTestSet = set(trainingSession.testSet)
        commonData = actualTrainingSet.intersection(actualTestSet)
        actualDataSet = actualTrainingSet.union(actualTestSet)
        self.assertSetEqual(commonData, set(), 'ERROR : test & training data collides')
        self.assertSetEqual(actualDataSet, expectedDataSet, 'ERROR : merged test & training data does not fill data set')