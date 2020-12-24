# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/fileToDataframe.py
# Compiled at: 2019-09-05 09:29:14
# Size of source mod 2**32: 1349 bytes
__all__ = [
 'filetodataframe']
import sys, os, pandas as pd

def vdeToDataframe(myvde):
    dimension = []
    region = []
    codset = []
    description = []
    with open(myvde) as (f):
        for line in f:
            line = line.split(',')
            dimension.append(line[0].split('"')[1])
            region.append(line[1].split('"')[1])
            codset.append(line[2].split('"')[1])
            description.append(line[3].split('"')[1])

    df = pd.DataFrame({'dimension':dimension,  'region':region, 
     'codset':codset,  'description':description})
    return df


def vdsToDataframe(myvde):
    dimension = []
    region = []
    codset = []
    dimensionCode = []
    with open(myvde) as (f):
        for line in f:
            line = line.split(',')
            dimension.append(line[0].split('"')[1])
            region.append(line[1].split('"')[1])
            codset.append(line[2].split('"')[1])
            dimensionCode.append(line[3].split('"')[1])

    df = pd.DataFrame({'dimension':dimension,  'region':region, 
     'codset':codset,  'dimensionCode':dimensionCode})
    return df


if __name__ == '__main__':
    myfile = sys.argv[1]
    df = vdsToDataframe(myfile)
    print(df)