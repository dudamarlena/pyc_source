# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/header_block.py
# Compiled at: 2020-02-14 18:47:56
# Size of source mod 2**32: 5091 bytes
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
import struct
from os import SEEK_CUR
from typing import IO
from collections import namedtuple
import numpy as np
__all__ = [
 'HeaderBlock',
 'read_header_block',
 'write_header_block',
 'compute_header_byte_size']
HeaderBlock = namedtuple('HeaderBlock', [
 'header_size',
 'block_size',
 'num_channels',
 'num_samples',
 'sampling_rate'])
PADDING = np.array([
 24, 0, 0, 0,
 1, 0, 0, 0,
 189, 0, 0, 0,
 0, 0, 0, 0,
 196, 63, 9, 0,
 0, 0, 0, 0,
 1, 1, 0, 0],
  dtype=(np.uint8)).tobytes()

def encode_rate_depth(rate: int, depth: int):
    """return joined rate and byte depth of samples

    Sampling rate and sample depth are encoded in a single 4-byte integer.  The
    first byte is the depth the last 3 bytes give the sampling rate.
    """
    if not depth < 256:
        raise AssertionError(f"depth must be smaller than 256 (got {depth})")
    elif not rate < 16777216:
        raise AssertionError(f"depth must be smaller than {16777216} (got {rate})")
    return (rate << 8) + depth


def decode_rate_depth(x: int):
    """return rate and depth from encoded representation"""
    rate = x >> 8
    depth = x & 255
    return (rate, depth)


def compute_header_byte_size(num_channels):
    return 4 * (4 + 2 * num_channels) + len(PADDING)


def read_header_block(filepointer: IO[bytes]):
    """return HeaderBlock, read from fp"""

    def read(format_str):
        num_bytes = struct.calcsize(format_str)
        byts = filepointer.read(num_bytes)
        ans = struct.unpack(format_str, byts)
        if len(ans) > 1:
            return ans
        else:
            return ans[0]

    def skip(n):
        filepointer.seek(n, SEEK_CUR)

    if read('i') == 0:
        return
    else:
        header_size, block_size, num_channels = read('3i')
        num_samples = block_size // num_channels // 4
        nc4 = 4 * num_channels
        skip(nc4)
        sampling_rate, depth = decode_rate_depth(read('i'))
        skip(nc4 - 4)
        assert depth == 32, f"\n    Unable to read MFF with `depth != 32` [`depth={depth}`]"
        padding_byte_size = header_size - 16 - 2 * nc4
        skip(padding_byte_size)
        return HeaderBlock(block_size=block_size,
          header_size=header_size,
          num_samples=num_samples,
          num_channels=num_channels,
          sampling_rate=sampling_rate)


def write_header_block(fp: IO[bytes], hdr: HeaderBlock):
    """write HeaderBlock `hdr` to file pointer `fp`"""
    fp.write(struct.pack('4i', 1, hdr.header_size, hdr.block_size, hdr.num_channels))
    num_samples = hdr.block_size // hdr.num_channels // 4
    arr = 4 * num_samples * np.arange(hdr.num_channels).astype(np.int32)
    fp.write(arr.tobytes())
    sr_d = encode_rate_depth(hdr.sampling_rate, 32)
    arr = sr_d * np.ones((hdr.num_channels), dtype=(np.int32))
    fp.write(arr.tobytes())
    pad_byte_len = hdr.header_size - 4 * (4 + 2 * hdr.num_channels)
    padding = PADDING if pad_byte_len == len(PADDING) else np.zeros(pad_byte_len, dtype=(np.uint8)).tobytes()
    fp.write(padding)