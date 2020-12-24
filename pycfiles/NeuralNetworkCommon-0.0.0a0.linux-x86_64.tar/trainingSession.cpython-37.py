# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/neuralnetworkcommon/trainingSession.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 4642 bytes
import pythoncommontools.objectUtil.POPO as POPO
from random import shuffle

class TrainingSessionProgress(POPO):

    @staticmethod
    def constructFromAttributes(meanDifferentialErrors, errorElementsNumbers, resets):
        trainingSessionProgress = TrainingSessionProgress()
        trainingSessionProgress.meanDifferentialErrors = meanDifferentialErrors
        trainingSessionProgress.errorElementsNumbers = errorElementsNumbers
        trainingSessionProgress.resets = resets
        return trainingSessionProgress


class TrainingSession(POPO):

    @staticmethod
    def constructFromTrainingSet(perceptronId, trainingSet, trainingChunkSize, saveInterval, maximumTry, maximumErrorRatio, testRatio, comments=''):
        trainingSession = TrainingSession()
        trainingSession.perceptronId = perceptronId
        trainingSession.trainingSetId = trainingSet.id
        trainingSession.trainingChunkSize = trainingChunkSize
        trainingSession.saveInterval = saveInterval
        trainingSession.maximumTry = maximumTry
        trainingSession.maximumErrorRatio = maximumErrorRatio
        trainingSession.comments = comments
        dataElements = trainingSet.trainingElements
        shuffle(dataElements)
        testSetLength = int(len(dataElements) * testRatio)
        trainingSession.testSet = dataElements[:testSetLength]
        trainingSession.trainingSet = dataElements[testSetLength:]
        return trainingSession

    @staticmethod
    def constructFromAttributes(perceptronId, trainingSetId, trainingChunkSize, saveInterval, maximumTry, maximumErrorRatio, trainingSet, testSet, pid, loadedLinesNumber, errorMessage, meanDifferentialErrors, errorElementsNumbers, resets, testScore, comments=''):
        trainingSession = TrainingSession()
        trainingSession.perceptronId = perceptronId
        trainingSession.trainingSetId = trainingSetId
        trainingSession.trainingChunkSize = trainingChunkSize
        trainingSession.saveInterval = saveInterval
        trainingSession.maximumTry = maximumTry
        trainingSession.maximumErrorRatio = maximumErrorRatio
        trainingSession.trainingSet = trainingSet
        trainingSession.testSet = testSet
        trainingSession.pid = pid
        trainingSession.loadedLinesNumber = loadedLinesNumber
        trainingSession.errorMessage = errorMessage
        trainingSession.meanDifferentialErrors = meanDifferentialErrors
        trainingSession.errorElementsNumbers = errorElementsNumbers
        trainingSession.resets = resets
        trainingSession.testScore = testScore
        trainingSession.comments = comments
        return trainingSession


class TrainingSessionSummary(POPO):

    @staticmethod
    def constructFromAttributes(trainingSetId, trainingChunkSize, saveInterval, maximumTry, maximumErrorRatio, trainingSetsNumber, testSetsNumber, pid, loadedLinesNumber, errorMessage, progressRecordsNumber, meanDifferentialErrors, errorElementsNumbers, resets, testScore, comments=''):
        trainingSessionSummary = TrainingSessionSummary()
        trainingSessionSummary.trainingSetId = trainingSetId
        trainingSessionSummary.trainingChunkSize = trainingChunkSize
        trainingSessionSummary.saveInterval = saveInterval
        trainingSessionSummary.maximumTry = maximumTry
        trainingSessionSummary.maximumErrorRatio = maximumErrorRatio
        trainingSessionSummary.trainingSetsNumber = trainingSetsNumber
        trainingSessionSummary.testSetsNumber = testSetsNumber
        trainingSessionSummary.pid = pid
        trainingSessionSummary.loadedLinesNumber = loadedLinesNumber
        trainingSessionSummary.errorMessage = errorMessage
        trainingSessionSummary.progressRecordsNumber = progressRecordsNumber
        trainingSessionSummary.meanDifferentialErrors = meanDifferentialErrors
        trainingSessionSummary.errorElementsNumbers = errorElementsNumbers
        trainingSessionSummary.resets = resets
        trainingSessionSummary.testScore = testScore
        trainingSessionSummary.comments = comments
        return trainingSessionSummary