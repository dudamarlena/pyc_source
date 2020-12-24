# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/dataloader.py
# Compiled at: 2019-01-07 11:15:30
# Size of source mod 2**32: 432 bytes
from torch.utils import data

class DataLoader(data.DataLoader):
    __doc__ = '\n    serializable dataloader\n    '

    def __init__(self, dataset, **kwargs):
        (super(DataLoader, self).__init__)(dataset, **kwargs)
        self.kwargs = kwargs
        self.dataset = dataset

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)