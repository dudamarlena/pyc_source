# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seeta_dataset/datacenter.py
# Compiled at: 2019-10-24 15:15:30
# Size of source mod 2**32: 430 bytes
from seeta_dataset.readonly_dataset import ReadOnlyDataset
from seeta_dataset.writeonly_dataset import WriteOnlyDataset

class DataCenter(object):

    def __init__(self, root):
        self._root = root

    def load_dataset(self, dataset_id):
        return ReadOnlyDataset(self._root, dataset_id)

    def create_dataset(self, record_type, dataset_id=None):
        return WriteOnlyDataset(self._root, dataset_id, record_type)