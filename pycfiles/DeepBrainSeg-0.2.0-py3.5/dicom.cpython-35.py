# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepBrainSeg/readers/dicom.py
# Compiled at: 2019-11-11 08:44:10
# Size of source mod 2**32: 1586 bytes
import os, tempfile
from time import time
import pydicom, datetime
from pydicom.dataset import Dataset, FileDataset
import numpy as np

class dcm_loader(object):
    __doc__ = '\n    '

    def __init__(self):
        pass

    def load_vol(self, path):
        """
            path : patient data path

            returns numpy array of patient data
        """
        self.patient = pydicom.dcmread(path)
        return self.patient.pixel_array

    def write_vol(self, path, vol):
        """
            path : path to write the data
            vol : modifient volume

            return: True or False based on saving of volume
        """
        suffix = '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
        filename_big_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
        file_meta = Dataset()
        ds = FileDataset(filename_little_endian, {}, file_meta=file_meta, preamble=b'\x00' * 128)
        ds.PatientName = self.patient.PatientName
        ds.PatientID = self.patient.PatientID
        ds.is_little_endian = self.patient.is_little_endian
        ds.is_implicit_VR = self.patient.is_implicit_VR
        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')
        ds.ContentTime = timeStr
        ds.PixelData = vol.tostring()
        try:
            ds.save_as(filename_little_endian)
            return True
        except:
            return False