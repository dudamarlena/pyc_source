# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/bin_writer.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 4758 bytes
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
from os import SEEK_SET
from io import BytesIO
from typing import List, Union
import numpy as np
from .epoch import Epoch
from .header_block import HeaderBlock, write_header_block, compute_header_byte_size

class BinWriter:
    default_filename = 'signal1.bin'
    default_info_filename = 'info1.xml'

    def __init__(self, sampling_rate: int, data_type: str='EEG'):
        """

        **Parameters**

        * **`sampling_rate`**: sampling rate of all channels.  Sampling rate
        has to fit in a 3-byte integer.  See docs in `mffpy.header_block`.

        * **`data_type`**: name of the type of signal.
        """
        self.data_type = data_type
        self.sampling_rate = sampling_rate
        self.header = None
        self.stream = BytesIO()
        self.epochs = []

    @property
    def sampling_rate(self) -> int:
        return self._sr

    @sampling_rate.setter
    def sampling_rate(self, sr: int) -> None:
        assert isinstance(sr, int), f"sampling rate not int. Received {sr}"
        self._sr = sr

    def get_info_kwargs(self):
        return {'filename':self.default_info_filename, 
         'fileDataType':self.data_type}

    def _add_block_to_epochs(self, num_samples, offset_us=0):
        """append `num_samples` to last epoch or make new epoch"""
        duration_us = int(1000000 * num_samples / self.sampling_rate)
        if len(self.epochs) == 0:
            self.epochs.append(Epoch(beginTime=offset_us,
              endTime=(offset_us + duration_us),
              firstBlock=1,
              lastBlock=1))
        else:
            if offset_us > 0:
                beginTime = self.epochs[(-1)].endTime + offset_us
                blockIdx = self.epochs[(-1)].lastBlock + 1
                self.epochs.append(Epoch(beginTime=beginTime,
                  endTime=(beginTime + duration_us),
                  firstBlock=blockIdx,
                  lastBlock=blockIdx))
            else:
                self.epochs[(-1)].add_block(duration_us)

    def add_block(self, data: np.ndarray, offset_us: int=0):
        """add a block of signal data after a time offset

        **Parameters**

        * *`data`*: float-32 signals array of shape `(num_channels,
        num_samples)`.

        * *`offset_us`*: microsecond offset to attach the signals after the
        last added block of data.  If `offset_us>0` there's a discontinuity in
        the recording.
        """
        num_channels, num_samples = data.shape
        assert data.dtype == np.float32
        if self.header is None:
            self.header = HeaderBlock(block_size=(4 * data.size),
              header_size=(compute_header_byte_size(num_channels)),
              num_samples=num_samples,
              num_channels=num_channels,
              sampling_rate=(self.sampling_rate))
        else:
            assert num_channels == self.header.num_channels
            self.header = HeaderBlock(block_size=(4 * data.size),
              header_size=(self.header.header_size),
              num_samples=num_samples,
              num_channels=num_channels,
              sampling_rate=(self.sampling_rate))
        write_header_block(self.stream, self.header)
        self.append(data.tobytes())
        self._add_block_to_epochs(num_samples, offset_us=offset_us)

    def append(self, b: bytes):
        """append bytes `b` to stream and check write"""
        num_written = self.stream.write(b)
        assert num_written == len(b), f"\n        Wrote {num_written} bytes (expected {len(b)})"

    def write(self, filename: str, *args, **kwargs):
        self.stream.seek(0, SEEK_SET)
        byts = self.stream.read()
        with open(filename, 'wb') as (fo):
            num_written = fo.write(byts)
        assert num_written == len(byts), f"\n        Wrote {num_written} bytes (expected {len(byts)})"