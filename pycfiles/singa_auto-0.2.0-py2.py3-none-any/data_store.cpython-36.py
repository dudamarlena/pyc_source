# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/data_store/data_store.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 1720 bytes
import abc, sys
from typing import List, Dict
import os

class Dataset:

    def __init__(self, id: str, size_bytes: int):
        self.id = id
        self.size_bytes = size_bytes


class DataStore(abc.ABC):
    __doc__ = '\n        Persistent store for datasets.\n    '

    @abc.abstractmethod
    def save(self, data_file_path: str) -> Dataset:
        """
            Persists a dataset in the local filesystem at file path, returning a ``Dataset`` abstraction containing a unique ID for the dataset.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, dataset_id: str) -> str:
        """
            Loads a persisted dataset to the local filesystem, identified by ID, returning the file path to the dataset.
        """
        raise NotImplementedError()

    @staticmethod
    def _get_size_bytes(data_file_path):
        st = os.stat(data_file_path)
        return st.st_size