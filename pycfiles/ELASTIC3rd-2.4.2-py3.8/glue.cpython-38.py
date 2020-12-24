# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\energy\glue.py
# Compiled at: 2020-01-13 09:44:26
# Size of source mod 2**32: 1322 bytes
import os, shutil, numpy as np

def write_energyrun(RunStr):
    EPath = os.path.dirname(__file__)
    FileName = EPath + '\\energyrun'
    fopen = open(FileName, 'w')
    fopen.write(RunStr)
    fopen.close()


def run():
    EPath = os.path.dirname(__file__)
    FileName = EPath + '\\energyrun'
    fopen = open(FileName, 'r')
    for eachline in fopen:
        eachline = eachline.strip('\n')
        RunStr = eachline.strip()
        print(RunStr)
    else:
        fopen.close()


def multi_energy(energy):
    EV2H = 0.0367493
    EV2KJ = 96.4853104
    EV2KC = 23.0605441
    Energy = np.array([energy, EV2H * energy, EV2KJ * energy, EV2KC * energy])
    return Energy


def DeleteFiles(path, remainDirsList, filesList):
    dirsList = []
    dirsList = os.listdir(path)
    for f in dirsList:
        if f not in remainDirsList:
            filePath = os.path.join(path, f)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath, True)
        if f in filesList:
            filepath = os.path.join(path, f)
            os.remove(f)