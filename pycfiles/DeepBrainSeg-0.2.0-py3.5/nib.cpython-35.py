# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepBrainSeg/readers/nib.py
# Compiled at: 2019-11-11 08:44:10
# Size of source mod 2**32: 731 bytes
import os, tempfile
from time import time
import datetime, numpy as np, nibabel as nib

class nib_loader(object):
    __doc__ = '\n    '

    def __init__(self):
        pass

    def load_vol(self, path):
        """
            path : patient data path

            returns numpy array of patient data
        """
        self.patient = nib.load(path)
        return self.patient.get_data()

    def write_vol(self, path, vol):
        """
            path : path to write the data
            vol : modifient volume

            return: True or False based on saving of volume
        """
        try:
            ds.save_as(filename_little_endian)
            return True
        except:
            return False