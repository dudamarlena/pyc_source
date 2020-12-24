# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Demos/geometry.py
# Compiled at: 2017-06-20 08:49:49
from __future__ import division
import numpy as np

class TIGREParameters:

    def __init__(self, high_quality=True):
        if high_quality:
            self.DSD = 1536
            self.DSO = 1000
            self.nDetector = np.array((512, 512))
            self.dDetector = np.array((0.8, 0.8))
            self.sDetector = self.nDetector * self.dDetector
            self.nVoxel = np.array((256, 256, 256))
            self.sVoxel = np.array((256, 256, 256))
            self.dVoxel = self.sVoxel / self.nVoxel
            self.offOrigin = np.array((0, 0, 0))
            self.offDetector = np.array((0, 0))
            self.accuracy = 0.5
            self.mode = 'cone'
        else:
            self.DSD = 1536
            self.DSO = 1000
            self.nDetector = np.array((128, 130))
            self.dDetector = np.array((0.8, 0.8)) * 4
            self.sDetector = self.nDetector * self.dDetector
            self.nVoxel = np.array((64, 64, 64))
            self.sVoxel = np.array((256, 256, 256))
            self.dVoxel = self.sVoxel / self.nVoxel
            self.offOrigin = np.array((0, 0, 0))
            self.offDetector = np.array((0, 0))
            self.accuracy = 0.5
            self.mode = None
            self.filter = None
        return

    def __str__(self):
        parameters = []
        parameters.append('TIGRE parameters')
        parameters.append('-----')
        parameters.append('Distance from source to detector = ' + str(self.DSD) + 'mm')
        parameters.append('Distance from source to origin = ' + str(self.DSO) + 'mm')
        parameters.append('-----')
        parameters.append('Detector parameters')
        parameters.append('Number of pixels = ' + str(self.nDetector))
        parameters.append('Size of each pixel = ' + str(self.dDetector) + 'mm')
        parameters.append('Total size of the detector = ' + str(self.sDetector) + 'mm')
        parameters.append('-----')
        parameters.append('Image parameters')
        parameters.append('Number of voxels = ' + str(self.nVoxel))
        parameters.append('Total size of the image = ' + str(self.sVoxel) + 'mm')
        parameters.append('Size of each voxel = ' + str(self.dVoxel) + 'mm')
        parameters.append('-----')
        parameters.append('Offset correction parameters')
        parameters.append('Offset of image from origin = ' + str(self.offOrigin) + 'mm')
        parameters.append('Offset of detector = ' + str(self.offDetector) + 'mm')
        parameters.append('-----')
        parameters.append('Auxillary parameters')
        parameters.append('Accuracy of forward projection = ' + str(self.accuracy))
        return ('\n').join(parameters)