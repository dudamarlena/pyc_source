# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/menorah/swarmtemplate.py
# Compiled at: 2015-10-24 14:05:10
import os, copy
SWARM_DESCRIPTION = {'includedFields': [
                    {'fieldName': 'timestamp', 
                       'fieldType': 'datetime'}], 
   'streamDef': {'info': 'kw_energy_consumption', 
                 'version': 1, 
                 'streams': [
                           {'info': '', 
                              'source': 'file://', 
                              'columns': [
                                        '*']}]}, 
   'inferenceType': 'TemporalMultiStep', 
   'inferenceArgs': {'predictionSteps': [
                                       1], 
                     'predictedField': ''}, 
   'iterationCount': 3000, 
   'swarmSize': 'medium'}
FIELD = {'fieldName': '', 
   'fieldType': 'float', 
   'maxValue': None, 
   'minValue': None}

def createSwarmDescription(fields, csvPath, predictedField, swarmParams=None):
    swarmDesc = copy.deepcopy(SWARM_DESCRIPTION)
    swarmDesc['includedFields'] = swarmDesc['includedFields'] + fields
    swarmDesc['inferenceArgs']['predictedField'] = predictedField
    outStream = swarmDesc['streamDef']['streams'][0]
    outStream['info'] = csvPath
    outStream['source'] = outStream['source'] + os.path.abspath(csvPath)
    if swarmParams is not None:
        swarmDesc.update(swarmParams)
    return swarmDesc