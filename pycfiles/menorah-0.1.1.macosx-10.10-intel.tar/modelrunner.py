# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/menorah/modelrunner.py
# Compiled at: 2015-10-26 18:00:54
import os
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager
import nupic_output
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def _createModel(modelParams, predictedField):
    model = ModelFactory.create(modelParams)
    model.enableInference({'predictedField': predictedField})
    return model


def _getModelParamsFromWorkDir(workingDir):
    modelParamsPath = os.path.join(workingDir, 'model_params', 'model_params.py')
    print 'Importing model params from %s' % modelParamsPath
    myGlobals = {'MODEL_PARAMS': None}
    execfile(modelParamsPath, myGlobals)
    return myGlobals['MODEL_PARAMS']


def createMetrics(predictedField):
    return (
     MetricSpec(field='', metric='multiStep', inferenceElement='multiStepBestPredictions', params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
     MetricSpec(field=predictedField, metric='trivial', inferenceElement='prediction', params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
     MetricSpec(field=predictedField, metric='multiStep', inferenceElement='multiStepBestPredictions', params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
     MetricSpec(field=predictedField, metric='trivial', inferenceElement='prediction', params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}))


def getRowHandlers(workingDirPath, predictedField, modelParams=None, plot=False):
    global counter
    if modelParams is None:
        print 'Creating model from %s...' % workingDirPath
        modelParams = _getModelParamsFromWorkDir(workingDirPath)
    else:
        print 'Creating model from previously loaded model params.'
    model = _createModel(modelParams, predictedField)
    shifter = InferenceShifter()
    if plot:
        output = nupic_output.NuPICPlotOutput([workingDirPath])
    else:
        output = nupic_output.NuPICFileOutput([workingDirPath])
    metricsManager = MetricsManager(createMetrics(predictedField), model.getFieldInfo(), model.getInferenceType())
    counter = 0

    def handler(headers, row):
        global counter
        dataDict = dict(zip(headers, row))
        result = model.run(dataDict)
        result.metrics = metricsManager.update(result)
        if counter % 100 == 0:
            print 'Read %i lines...' % counter
            print 'After %i records, 1-step altMAPE=%f' % (counter,
             result.metrics[("multiStepBestPredictions:multiStep:errorMetric='altMAPE':steps=1:window=1000:field=%s" % predictedField)])
        counter += 1
        if plot:
            result = shifter.shift(result)
        prediction = result.inferences['multiStepBestPredictions'][1]
        timestamp = row[0]
        value = row[headers.index(predictedField)]
        output.write([timestamp], [value], [prediction])

    def whenDone():
        output.close()

    return (
     handler, whenDone)