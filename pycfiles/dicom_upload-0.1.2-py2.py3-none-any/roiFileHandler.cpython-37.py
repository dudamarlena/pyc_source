# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/roiFileHandler.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1538 bytes
from __future__ import print_function
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

import dicom_tools.roiData as roiData

class roiFileHandler:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.dicomsPath = None

    def write(self, filename, roistates, numberOfROIs):
        tobesaved = roiData(roistates, numberOfROIs, self.dicomsPath)
        with open(filename, 'w') as (file):
            pickle.dump(tobesaved, file)
        file.close()

    def read(self, filename):
        if self.verbose:
            print('roiFileHandler: reading file ' + filename + '\n')
        with open(filename, 'r') as (file):
            buffer = pickle.load(file)
            file.close()
        self.dicomsPath = buffer.dicomsPath
        roistates = [None] * buffer.originalLenght
        for i, roistate in zip(buffer.layers, buffer.roistates):
            roistates[i] = roistate

        if self.verbose:
            print('roiFileHandler: returning \n')
        return (roistates, buffer.numberOfROIs)