# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/raw_bin_files.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 8064 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
import itertools
from os import SEEK_SET, SEEK_CUR, SEEK_END
from typing import Tuple, Dict, IO, Union
from collections import namedtuple
import numpy as np
from cached_property import cached_property
from .header_block import read_header_block
DataBlock = namedtuple('DataBlock', 'byte_offset byte_size')

class RawBinFile:

    def __init__(self, filepointer: IO[bytes]):
        self.filepointer = filepointer
        assert not self.filepointer.closed
        self.buffering = False

    def __del__(self):
        self.close()

    def close(self):
        self.filepointer.close()

    def tell(self) -> int:
        return self.filepointer.tell()

    def seek(self, loc, mode=SEEK_SET):
        if not mode != SEEK_SET:
            if not loc >= 0:
                raise AssertionError
        if not mode != SEEK_END:
            if not loc <= 0:
                raise AssertionError
        return self.filepointer.seek(loc, mode)

    @cached_property
    def bytes_in_file(self):
        loc = self.tell()
        self.seek(0, mode=SEEK_END)
        bytes_in_file = self.tell()
        self.seek(loc, mode=SEEK_SET)
        return bytes_in_file

    @property
    def num_channels(self) -> int:
        return self.signal_blocks['num_channels']

    @property
    def sampling_rate(self) -> float:
        return self.signal_blocks['sampling_rate']

    @property
    def num_samples(self) -> int:
        """returns number of samples per channel in file"""
        return self.block_start_idx[(-1)]

    @property
    def duration(self) -> float:
        """returns duration of file in seconds"""
        return self.num_samples / self.sampling_rate

    @cached_property
    def signal_blocks(self) -> Dict[(str, Union[(int, float, list)])]:
        """return dictionary describing the signal file

        This cached property reads through all headers in the blocked binary
        structure.  Each block can have a varying number of samples.
        """
        num_samples, num_channels, header_sizes, sampling_rate, data = ([], [], [], [], [])
        hdr = None
        self.seek(0)
        for block_idx in itertools.count():
            if self.tell() >= self.bytes_in_file:
                break
            else:
                hdr = read_header_block(self.filepointer) or hdr
                assert hdr is not None, 'First block must be a header'
            sampling_rate.append(hdr.sampling_rate)
            num_channels.append(hdr.num_channels)
            data.append(DataBlock(self.tell(), hdr.block_size))
            num_samples.append(hdr.num_samples)
            header_sizes.append(hdr.header_size)
            self._skip_over(hdr.block_size)

        if not hdr is not None:
            raise AssertionError
        else:
            if not all(n == num_channels[0] for n in num_channels):
                raise AssertionError('\n        Found different channel number while reading header blocks')
            elif not all(sr == sampling_rate[0] for sr in sampling_rate):
                raise AssertionError('\n        Found different sampling rates while reading blocks')
            assert len(num_samples) > 0, f"\n        No data found [`num_samples={num_samples}`]"
        return {'data':data, 
         'n_blocks':block_idx, 
         'num_samples':num_samples, 
         'num_channels':num_channels[0], 
         'header_sizes':header_sizes, 
         'sampling_rate':sampling_rate[0]}

    def _skip_over(self, block_size: int):
        """Skip filepointer over `block_size` bytes"""
        self.seek(block_size, mode=SEEK_CUR)

    @cached_property
    def block_start_idx(self) -> np.ndarray:
        return np.cumsum([
         0] + self.signal_blocks['num_samples'])

    def _read_blocks(self, A: int, B: int) -> np.ndarray:
        """return data of all blocks in range [A, B)

        Data of all channels are read and transformed into
        little-endian 4-bit floats.  Then they are reshaped to
        `(num_channels, num_samples)` with row-major ordering:

        ```
        x = array([[ch0 smp0, ch0 smp1, ch0...],
                   [ch1 smp0, ch1 smp1, ch1...]])
        ```
        These data lie in memory like:
        `[x[0,0], x[0,1], .. x[0,n], x[1,0], x[1,1], .. x[1,n]]`

        """
        data = []
        for block in self.signal_blocks['data'][A:B]:
            self.seek(block.byte_offset)
            buf = self.filepointer.read(block.byte_size)
            d = np.frombuffer(buf, '<f4', count=(-1))
            d = d.reshape((self.num_channels), (-1), order='C')
            data.append(d)

        return np.concatenate(data, axis=1)

    def read_raw_samples(self, t0: float=0.0, dt: float=None, block_slice: slice=None) -> Tuple[(np.ndarray, float)]:
        """return `(channels, samples)`-array and `start_time` of data

        The signal data is organized in variable-sized blocks that enclose
        epochs of continuous recordings.  Discontinuous breaks can happen in
        between blocks.  `block_slice` indexes into such epochs if not None,
        but we might want only a small chunk of it given by `t0` and `dt`.
        Therefore, we further index into blocks `bsi` selected through
        block_slice with the variables `A` and `B`.  Block indices `A` and `B`
        are chosen to enclose the interval `(t0, t0+dt)` which we would like to
        read.

        **Parameters**
        t0: float (default: 0.0)
            Start time to read out data, starting at the beginning of the
            block.
        dt: float (default: None)
            duration of the data to read out.  `None` defaults to the rest of
            the signal.
        block_slice: slice (default: None)
            blocks to consider when reading data.

        **Returns**
        block_data: np.ndarray
            array containing all samples between the samples enclosing
            `(t0,t0+dt)` relative to the block slice.
        time_of_first_sample: float
            time in seconds from file start of the first returned sample.
        """
        if not block_slice is None:
            if not isinstance(block_slice, slice):
                raise AssertionError
        else:
            block_slice = block_slice if block_slice else slice(0, len(self.block_start_idx) - 1)
            sr = self.signal_blocks['sampling_rate']
            a = np.round(t0 * sr).astype(int) if t0 is not None else None
            b = np.round((t0 + dt) * sr).astype(int) if dt is not None else None
            time_of_first_sample = a / sr
            bsi = self.block_start_idx[block_slice]
            A = bsi.searchsorted((bsi[0] + a), side='right') - 1 if a is not None else 0
            B = bsi.searchsorted((bsi[0] + b), side='left') if b is not None else len(bsi)
            if a is not None:
                a -= bsi[A] - bsi[0]
            if b is not None:
                b -= bsi[A] - bsi[0]
        A += block_slice.start
        B += block_slice.start
        block_data = self._read_blocks(A, B)
        block_data = block_data[:, a:b]
        return (block_data, time_of_first_sample)