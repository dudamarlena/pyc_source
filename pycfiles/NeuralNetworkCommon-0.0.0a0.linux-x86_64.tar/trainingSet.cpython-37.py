# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/neuralnetworkcommon/trainingSet.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 1071 bytes
import pythoncommontools.objectUtil.POPO as POPO

class TrainingSet(POPO):

    @staticmethod
    def constructFromAttributes(id, trainingElements, workspaceId=None, comments=''):
        trainingSet = TrainingSet()
        trainingSet.id = id
        trainingSet.workspaceId = workspaceId
        trainingSet.trainingElements = trainingElements
        trainingSet.comments = comments
        return trainingSet


class TrainingSetSummary(POPO):

    @staticmethod
    def constructFromAttributes(workspaceId, trainingElementsNumber, comments=''):
        trainingSetSummary = TrainingSetSummary()
        trainingSetSummary.workspaceId = workspaceId
        trainingSetSummary.trainingElementsNumber = trainingElementsNumber
        trainingSetSummary.comments = comments
        return trainingSetSummary