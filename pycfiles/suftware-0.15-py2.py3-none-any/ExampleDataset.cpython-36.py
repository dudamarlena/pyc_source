# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13_pip_test/suftware/src/ExampleDataset.py
# Compiled at: 2018-04-12 16:25:55
# Size of source mod 2**32: 2193 bytes
import numpy as np
from suftware.src.utils import ControlledError, check, handle_errors
import os
data_dir = os.path.dirname(os.path.abspath(__file__)) + '/../examples/data'
VALID_DATASETS = ['.'.join(name.split('.')[:-1]) for name in os.listdir(data_dir) if '.txt' in name]
VALID_DATASETS.sort()

class ExampleDataset:
    __doc__ = '\n    Provides an interface to example data provided with the SUFTware package.\n\n    parameters\n    ----------\n\n    dataset: (str)\n        Name of dataset to load. Run sw.ExampleDataset.list() to see\n        which datasets are available.\n\n    attributes\n    ----------\n\n    data: (np.array)\n        An array containing sampled data\n\n    details: (np.array, optional)\n        Optional return value containing meta information\n\n\n    '

    @handle_errors
    def __init__(self, dataset='old_faithful_eruption_times'):
        check(dataset in self.list(), 'Distribution "%s" not recognized.' % dataset)
        file_name = '%s/%s.txt' % (data_dir, dataset)
        self._load_dataset(file_name)

    @handle_errors
    def _load_dataset(self, file_name):
        self.data = np.genfromtxt(file_name)
        details = {}
        header_lines = [line.strip()[1:] for line in open(file_name, 'r') if line.strip()[0] == '#']
        for line in header_lines:
            key = eval(line.split(':')[0])
            value = eval(line.split(':')[1])
            try:
                setattr(self, key, value)
            except:
                ControlledError('Error loading example data. Either key or valueof metadata is invalid. key = %s, value = %s' % (
                 key, value))

    @staticmethod
    @handle_errors
    def list():
        """
        Return list of available datasets.
        """
        return VALID_DATASETS