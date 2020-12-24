# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/utils/struct_helpers.py
# Compiled at: 2018-08-15 14:22:35
# Size of source mod 2**32: 4190 bytes
"""
Author: Keith Bourgoin, Emmett Butler
"""
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['unpack_from']
import itertools, struct
from .compat import range

def unpack_from(fmt, buff, offset=0):
    """A customized version of `struct.unpack_from`

    This is a conveinence function that makes decoding the arrays,
    strings, and byte arrays that we get from Kafka significantly
    easier. It takes the same arguments as `struct.unpack_from` but
    adds 3 new formats:

    * Wrap a section in `[]` to indicate an array. e.g.: `[ii]`
    * `S` for strings (int16 followed by byte array)
    * `Y` for byte arrays (int32 followed by byte array)

    Spaces are ignored in the format string, allowing more readable formats

    NOTE: This may be a performance bottleneck. We're avoiding a lot of memory
          allocations by using the same buffer, but if we could call
          `struct.unpack_from` only once, that's about an order of magnitude
          faster. However, constructing the format string to do so would erase
          any gains we got from having the single call.
    """
    fmt = fmt.replace(' ', '')
    if fmt[0] in '!><':
        fmt = fmt[1:]
    output = _unpack(fmt, buff, offset, 1)[0]
    if fmt[0] == '[':
        if len(output) == 1:
            output = output[0]
    return output


def _unpack(fmt, buff, offset, count=1):
    """Recursive call for unpacking

    :param fmt: The struct format string
    :type fmt: str
    :param buff: The buffer into which to unpack
    :type buff: buffer
    :param offset: The offset at which to start unpacking
    :type offset: int
    :param count: The number of items in the array
    :type count: int
    """
    items = []
    array_fmt = None
    for i, ch in enumerate(fmt):
        if array_fmt is not None:
            if ch == ']':
                if array_fmt.count('[') == array_fmt.count(']'):
                    count = struct.unpack_from('!i', buff, offset)[0]
                    array_item, offset = _unpack_array(array_fmt, buff, offset + 4, count)
                    items.append(array_item)
                    array_fmt = None
                    continue
            array_fmt += ch
        elif ch == '[':
            array_fmt = ''
        else:
            if ch in 'SY':
                len_fmt = '!h' if ch == 'S' else '!i'
                len_ = struct.unpack_from(len_fmt, buff, offset)[0]
                offset += struct.calcsize(len_fmt)
                if len_ == -1:
                    items.append(None)
                    continue
                ch = '%ds' % len_
            items.extend(struct.unpack_from('!' + ch, buff, offset))
            offset += struct.calcsize(ch)

    return (
     tuple(items), offset)


def _unpack_array(fmt, buff, offset, count):
    """Unpack an array of items.

    :param fmt: The struct format string
    :type fmt: str
    :param buff: The buffer into which to unpack
    :type buff: buffer
    :param offset: The offset at which to start unpacking
    :type offset: int
    :param count: The number of items in the array
    :type count: int
    """
    output = []
    for i in range(count):
        item, offset = _unpack(fmt, buff, offset)
        output.append(item)

    if len(fmt) == 1:
        output = list(itertools.chain.from_iterable(output))
    return (
     output, offset)