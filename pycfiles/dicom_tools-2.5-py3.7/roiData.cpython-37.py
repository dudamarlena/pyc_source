# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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