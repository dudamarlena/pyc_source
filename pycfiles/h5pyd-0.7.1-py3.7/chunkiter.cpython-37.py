# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/chunkiter.py
# Compiled at: 2019-12-23 20:32:48
# Size of source mod 2**32: 2910 bytes


class ChunkIterator:
    __doc__ = '\n    Class to iterate through list of chunks given h5py dset\n    '

    def __init__(self, dset):
        self._shape = dset.shape
        if dset.chunks is None:
            self._layout = dset.shape
        else:
            self._layout = dset.chunks
        self._rank = len(dset.shape)
        if self._rank == 0:
            self._chunk_index = [
             0]
        else:
            self._chunk_index = [
             0] * self._rank

    def __iter__(self):
        return self

    def __next__(self):

        def get_ret(item):
            if len(item) == 1:
                return item[0]
            return tuple(item)

        if self._layout is ():
            if self._chunk_index[0] > 0:
                raise StopIteration()
            self._chunk_index[0] += 1
            return ()
        slices = []
        if self._chunk_index[0] * self._layout[0] >= self._shape[0]:
            raise StopIteration()
        for dim in range(self._rank):
            start = self._chunk_index[dim] * self._layout[dim]
            stop = start + self._layout[dim]
            if stop > self._shape[dim]:
                stop = self._shape[dim]
            s = slice(start, stop, 1)
            slices.append(s)

        dim = self._rank - 1
        while dim >= 0:
            c = self._layout[dim]
            self._chunk_index[dim] += 1
            chunk_end = self._chunk_index[dim] * c
            if chunk_end < self._shape[dim]:
                return get_ret(slices)
            if dim > 0:
                self._chunk_index[dim] = 0
            dim -= 1

        return get_ret(slices)