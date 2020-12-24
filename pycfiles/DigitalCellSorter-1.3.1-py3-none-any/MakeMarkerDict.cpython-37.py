# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_DCS\VS\DigitalCellSorter\dev\DigitalCellSorter\MakeMarkerDict.py
# Compiled at: 2019-09-03 17:31:40
# Size of source mod 2**32: 1776 bytes
"""
Created on Tue Feb 06 09:43:38 2018

@author: szedlak1
"""
import pandas as pd, numpy as np
from .GeneNameConverter import GeneNameConverter

def MakeMarkerDict(geneListDir, gnc=None):
    markerDict = {}
    markerDictnegative = {}
    df = pd.read_excel(geneListDir).replace(np.nan, 0).replace('+', 1).replace('-', -1)
    df['Marker'] = [i.strip('*') for i in df['Marker']]
    if gnc is not None:
        officialHugos = gnc.Convert([str(i) for i in df['Marker']], 'alias', 'hugo', returnUnknownString=False)
        hugo_cd_dict = dict(zip(officialHugos, df['Marker']))
        hugo_cd_dict.update(dict(zip(df['Marker'], officialHugos)))
        df['Marker'] = officialHugos
    for i in range(df.shape[0]):
        for j in df.columns[1:]:
            if df[j][i] == 1:
                try:
                    markerDict[df['Marker'][i]].append(j)
                except KeyError:
                    markerDict[df['Marker'][i]] = [
                     j]

    for key in markerDict.keys():
        markerDict[key] = list(set(markerDict[key]))

    for key in markerDictnegative.keys():
        markerDictnegative[key] = list(set(markerDictnegative[key]))

    if gnc is not None:
        return (
         markerDict, markerDictnegative, hugo_cd_dict)
    return markerDict