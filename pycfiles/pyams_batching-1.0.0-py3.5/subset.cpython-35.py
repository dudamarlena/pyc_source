# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_batching/subset.py
# Compiled at: 2019-12-24 06:06:49
# Size of source mod 2**32: 3353 bytes
"""PyAMS_batching.subset module

Batching implementation for subsets.

Sometimes subsets can have pre-batched values.
"""
from pyams_batching.batch import Batch, Batches
__docformat__ = 'restructuredtext'

class EmptyBatch(Batch):
    __doc__ = 'Empty batch'

    def __init__(self, length, start, size, batches):
        self.update(length, start, size)
        self.batches = batches

    def __eq__(self, other):
        return (
         self.size, self.start, self._length) == (
         other.size, other.start, other._length)

    @property
    def first_element(self):
        raise ValueError('EmptyBatch holds no item')

    @property
    def last_element(self):
        raise ValueError('EmptyBatch holds no item')

    def __getitem__(self, key):
        raise ValueError('EmptyBatch holds no item')

    def __iter__(self):
        raise ValueError('EmptyBatch holds no item')


class SubsetBatches(Batches):
    __doc__ = 'Subset batches'

    def __init__(self, batch):
        super(SubsetBatches, self).__init__(batch)
        self.length = batch._length

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self.total))
        if key not in self._batches:
            if key < 0:
                key = self.total + key
            batch = EmptyBatch(self.length, key * self.size, self.size, self)
            self._batches[batch.index] = batch
        try:
            return self._batches[key]
        except KeyError:
            raise IndexError(key)


class SubsetBatch(Batch):
    __doc__ = 'Subset batch'

    def __init__(self, sequence, length, start=0, size=20, batches=None):
        self.sequence = sequence
        self.update(length, start, size)
        self.update_batches(batches)

    def update_batches(self, batches):
        if batches is None:
            batches = SubsetBatches(self)
        self.batches = batches

    @property
    def first_element(self):
        """See interfaces.IBatch"""
        return self.sequence[0]

    @property
    def last_element(self):
        """See interfaces.IBatch"""
        return self.sequence[(-1)]

    def __getitem__(self, key):
        """See zope.interface.common.sequence.IMinimalSequence"""
        if isinstance(key, slice):
            return self.__getslice__(*key.indices(self._true_size))
        if key >= self._true_size:
            raise IndexError('batch index out of range')
        return self.sequence[key]

    def __iter__(self):
        """See zope.interface.common.sequence.IMinimalSequence"""
        return iter(self.sequence)

    def __eq__(self, other):
        return (
         self.size, self.start, self._length) == (
         other.size, other.start, other._length)