# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/roiData.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 429 bytes


class roiData:

    def __init__(self, roistates, numberOfROIs, dicomsPath=None):
        self.layers = []
        self.roistates = []
        self.dicomsPath = dicomsPath
        self.originalLenght = len(roistates)
        self.numberOfROIs = numberOfROIs
        for i, roistate in enumerate(roistates):
            if roistate:
                self.layers.append(i)
                self.roistates.append(roistate)