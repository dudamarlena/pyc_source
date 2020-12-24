# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/calibration.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 1868 bytes
import os, numpy as np
from pesummary import conf
from pesummary.utils.utils import logger, check_file_exists_and_rename

class Calibration(np.ndarray):
    __doc__ = 'Class to handle Calibration data\n    '

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if obj.shape[1] != 7:
            raise ValueError('Invalid input data. See the docs for instructions')
        return obj

    def save_to_file(self, file_name):
        """Save the calibration data to file

        Parameters
        ----------
        file_name: str
            name of the file name that you wish to use
        """
        check_file_exists_and_rename(file_name)
        header = [
         'Frequency', 'Median Mag', 'Phase (Rad)', '-1 Sigma Mag',
         '-1 Sigma Phase', '+1 Sigma Mag', '+1 Sigma Phase']
        np.savetxt(file_name,
          self, delimiter=(conf.delimiter), header=(conf.delimiter.join(header)),
          comments='')

    def __array_finalize__(self, obj):
        if obj is None:
            return