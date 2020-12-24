# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/dataset/dataset.py
# Compiled at: 2016-04-20 00:05:45
from abc import ABCMeta, abstractmethod
import collections

class Dataset(object):
    """
    Abstract dataset class.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def train_set(self):
        """
        :rtype: list of tuple
        """
        pass

    def valid_set(self):
        """
        :rtype: list of tuple
        """
        pass

    def test_set(self):
        """
        :rtype: list of tuple
        """
        pass

    def train_size(self):
        """
        Return size of training data. (optional)
        :rtype: number
        """
        train_set = self.train_set()
        if isinstance(train_set, collections.Iterable):
            return len(list(train_set))
        else:
            return
            return