# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/nrrdFileHandler.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 778 bytes
import numpy as np, nrrd

class nrrdFileHandler:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def read(self, inFileName):
        nrrdROItmp, nrrdROIoptions = nrrd.read(inFileName)
        nrrdROI = nrrdROItmp.swapaxes(0, 1).swapaxes(0, 2)
        return nrrdROI[::-1, :, ::-1]

    def write(self, outFileName, data):
        if self.verbose:
            print('nrrdFileHandler: type(data)', type(data), 'len(data)', len(data))
        outData = data.astype(int)
        outData = outData[::-1, :, :]
        outData = outData[:, :, ::-1]
        outData = outData.swapaxes(0, 2).swapaxes(0, 1)
        if not str(outFileName).endswith('.nrrd'):
            filename = outFileName + '.nrrd'
        nrrd.write(outFileName, outData)