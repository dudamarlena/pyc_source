# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: suftware/src/ExampleDataset.py
# Compiled at: 2018-04-12 16:25:55
import numpy as np
from suftware.src.utils import ControlledError, check, handle_errors
import os
data_dir = os.path.dirname(os.path.abspath(__file__)) + '/../examples/data'
VALID_DATASETS = [ ('.').join(name.split('.')[:-1]) for name in os.listdir(data_dir) if '.txt' in name
                 ]
VALID_DATASETS.sort()

class ExampleDataset:
    """
    Provides an interface to example data provided with the SUFTware package.

    parameters
    ----------

    dataset: (str)
        Name of dataset to load. Run sw.ExampleDataset.list() to see
        which datasets are available.

    attributes
    ----------

    data: (np.array)
        An array containing sampled data

    details: (np.array, optional)
        Optional return value containing meta information

    """

    @handle_errors
    def __init__(self, dataset='old_faithful_eruption_times'):
        check(dataset in self.list(), 'Distribution "%s" not recognized.' % dataset)
        file_name = '%s/%s.txt' % (data_dir, dataset)
        self._load_dataset(file_name)

    @handle_errors
    def _load_dataset(self, file_name):
        self.data = np.genfromtxt(file_name)
        details = {}
        header_lines = [ line.strip()[1:] for line in open(file_name, 'r') if line.strip()[0] == '#'
                       ]
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