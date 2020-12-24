# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/neuralnetworkcommon/service.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 1981 bytes
from enum import Enum, unique

@unique
class ContentType(Enum):
    JSON = 'application/json'
    GZIP = 'application/gzip'


@unique
class TrainerResourceValueType(Enum):
    WORKSPACE = '<int:workspaceId>'
    PERCEPTRON = '<int:perceptronId>'
    TRAININGSET = '<int:trainingSetId>'


@unique
class Parameters(Enum):
    TRAINING_SET_ID = 'trainingSetId'
    TRAINING_CHUNK_SIZE = 'trainingChunkSize'
    SAVE_INTERVAL = 'saveInterval'
    MAXIMUM_TRY = 'maximumTry'
    MAXIMUM_ERROR_RATIO = 'maximumErrorRatio'
    TEST_RATIO = 'testRatio'
    WORKSPACE_ID = 'workspaceId'
    COMMENTS = 'comments'
    DIMENSIONS = 'dimensions'


@unique
class TrainerResourcePathType(Enum):
    GLOBAL_WORKSPACE = '/'.join(('workspace', ))
    SPECIFIC_WORKSPACE = '/'.join((GLOBAL_WORKSPACE, TrainerResourceValueType.WORKSPACE.value))
    GLOBAL_PERCEPTRON = '/'.join(('perceptron', ))
    SPECIFIC_PERCEPTRON = '/'.join((GLOBAL_PERCEPTRON, TrainerResourceValueType.PERCEPTRON.value))
    SUMMARY = 'summary'
    PERCEPTRON_SUMMARY = '/'.join((GLOBAL_PERCEPTRON, TrainerResourceValueType.PERCEPTRON.value, SUMMARY))
    RANDOM = 'random'
    RANDOM_PERCEPTRON = '/'.join((GLOBAL_PERCEPTRON, RANDOM))
    GLOBAL_TRAININGSET = '/'.join(('trainingset', ))
    SPECIFIC_TRAININGSET = '/'.join((GLOBAL_TRAININGSET, TrainerResourceValueType.TRAININGSET.value))
    TRAININGSET_SUMMARY = '/'.join((SPECIFIC_TRAININGSET, SUMMARY))
    TRAINING_SESSION = 'trainingsession'
    GLOBAL_TRAININGSESSION = '/'.join((GLOBAL_PERCEPTRON, TRAINING_SESSION))
    SPECIFIC_TRAININGSESSION = '/'.join((GLOBAL_PERCEPTRON, TrainerResourceValueType.PERCEPTRON.value, TRAINING_SESSION))
    TRAININGSESSION_SUMMARY = '/'.join((SPECIFIC_TRAININGSESSION, SUMMARY))
    RANDOM_TRAININGSESSION = '/'.join((GLOBAL_TRAININGSESSION, RANDOM))
    TRAINER = '/'.join((GLOBAL_PERCEPTRON, TrainerResourceValueType.PERCEPTRON.value, 'trainer'))


@unique
class TrainerAction(Enum):
    ACTION = 'action'
    START = 'start'
    STOP = 'stop'