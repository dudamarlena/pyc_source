# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\drgpom\methods\biomarkers\davidson_biomarkers.py
# Compiled at: 2018-07-22 06:18:48
# Size of source mod 2**32: 2279 bytes
"""
Created on Fri Mar 11 12:56:55 2016

@author: Oliver Britton
"""
import pandas as pd

def CalibrationData(num_stds=1.0):
    lowerRanges = {}
    upperRanges = {}
    completeDict = {}
    for key in DavMeans:
        lowerRanges = DavMeans[key] - num_stds * DavStds[key]
        upperRanges = DavMeans[key] + num_stds * DavStds[key]
        completeDict[key] = [DavMeans[key], DavStds[key], lowerRanges, upperRanges]

    davData = pd.DataFrame(completeDict, columns)
    davData = davData.unstack().unstack()
    return davData


def GetCalibrationRanges():
    data = CalibrationData()
    calibrationRanges = data[['Min', 'Max']]
    return calibrationRanges


biomarkerNames = [
 'RMP', 'InputRes', 'RampAP', 'StepRheobase', 'Threshold', 'APPeak', 'APRise', 'APSlopeMin',
 'APSlopeMax', 'APFullWidth', 'AHPAmp', 'AHPTrough', 'AHPTau', 'numAPs']
columns = [
 'Mean', 'Std', 'Min', 'Max']
DavMeans = {}
DavMeans['RMP'] = -62.36
DavMeans['InputRes'] = 97.51
DavMeans['RampAP'] = 2.45
DavMeans['Rheobase'] = 1.43
DavMeans['Threshold'] = -15.73
DavMeans['APPeak'] = 64.64
DavMeans['APRiseTime'] = 0.5284
DavMeans['APSlopeMax'] = 326.9
DavMeans['APSlopeMin'] = -100.2
DavMeans['APFullWidth'] = 4.92
DavMeans['AHPAmp'] = -52.66
DavMeans['AHPTrough'] = DavMeans['AHPAmp']
DavMeans['AHPTau'] = 26.67
DavStds = {}
DavStds['RMP'] = 23.3
DavStds['InputRes'] = 111.4
DavStds['RampAP'] = 2.24
DavStds['Rheobase'] = 1.16
DavStds['Threshold'] = 10.0
DavStds['APPeak'] = 9.38
DavStds['APRiseTime'] = 0.35960000000000003
DavStds['APSlopeMax'] = 169.4
DavStds['APSlopeMin'] = 78.3
DavStds['APFullWidth'] = 3.73
DavStds['AHPAmp'] = 8.73
DavStds['AHPTrough'] = DavStds['AHPAmp']
DavStds['AHPTau'] = 22.1
biomarker_names = sorted(DavMeans.keys())
biomarkerNames = biomarker_names
davData = CalibrationData()