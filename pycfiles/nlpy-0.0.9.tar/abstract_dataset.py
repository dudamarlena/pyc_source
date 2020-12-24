# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/dataset/abstract_dataset.py
# Compiled at: 2014-12-16 21:08:45


class AbstractDataset(object):

    def __init__(self, target_format=None):
        self.target_format = target_format
        self._target_size = 0

    def _target_map(self, i):
        if self.target_format == 'vector' and self._target_size > 0:
            l = [
             0.0] * self._target_size
            l[i] = 1.0
            return l
        else:
            if self.target_format == 'tuple':
                return [i]
            if self.target_format == 'number':
                return i
            return i

    def train_set(self):
        """
        :rtype: tuple
        """
        pass

    def valid_set(self):
        """
        :rtype: tuple
        """
        pass

    def test_set(self):
        """
        :rtype: tuple
        """
        pass