# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/ledgerWrapper.py
# Compiled at: 2020-02-12 12:44:57
"""
*******************************************************************************
*   BTChip Bitcoin Hardware Wallet Python API
*   (c) 2014 BTChip - 1BTChip7VfTnrPra5jqci7ejnMguuHogTn
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*   Unless required by applicable law or agreed to in writing, software
*   distributed under the License is distributed on an "AS IS" BASIS,
*   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*   limitations under the License.
********************************************************************************
"""
import struct
from .navhipException import BTChipException

def wrapCommandAPDU(channel, command, packetSize):
    if packetSize < 3:
        raise BTChipException("Can't handle Ledger framing with less than 3 bytes for the report")
    sequenceIdx = 0
    offset = 0
    result = struct.pack('>HBHH', channel, 5, sequenceIdx, len(command))
    sequenceIdx = sequenceIdx + 1
    if len(command) > packetSize - 7:
        blockSize = packetSize - 7
    else:
        blockSize = len(command)
    result += command[offset:offset + blockSize]
    offset = offset + blockSize
    while offset != len(command):
        result += struct.pack('>HBH', channel, 5, sequenceIdx)
        sequenceIdx = sequenceIdx + 1
        if len(command) - offset > packetSize - 5:
            blockSize = packetSize - 5
        else:
            blockSize = len(command) - offset
        result += command[offset:offset + blockSize]
        offset = offset + blockSize

    while len(result) % packetSize != 0:
        result += '\x00'

    return bytearray(result)


def unwrapResponseAPDU(channel, data, packetSize):
    sequenceIdx = 0
    offset = 0
    if data is None or len(data) < 12:
        return
    if struct.unpack('>H', data[offset:offset + 2])[0] != channel:
        raise BTChipException('Invalid channel')
    offset += 2
    if data[offset] != 5:
        raise BTChipException('Invalid tag')
    offset += 1
    if struct.unpack('>H', data[offset:offset + 2])[0] != sequenceIdx:
        raise BTChipException('Invalid sequence')
    offset += 2
    responseLength = struct.unpack('>H', data[offset:offset + 2])[0]
    offset += 2
    if len(data) < 7 + responseLength:
        return
    else:
        if responseLength > packetSize - 7:
            blockSize = packetSize - 7
        else:
            blockSize = responseLength
        result = data[offset:offset + blockSize]
        offset += blockSize
        while len(result) != responseLength:
            sequenceIdx = sequenceIdx + 1
            if offset == len(data):
                return
            if struct.unpack('>H', data[offset:offset + 2])[0] != channel:
                raise BTChipException('Invalid channel')
            offset += 2
            if data[offset] != 5:
                raise BTChipException('Invalid tag')
            offset += 1
            if struct.unpack('>H', data[offset:offset + 2])[0] != sequenceIdx:
                raise BTChipException('Invalid sequence')
            offset += 2
            if responseLength - len(result) > packetSize - 5:
                blockSize = packetSize - 5
            else:
                blockSize = responseLength - len(result)
            result += data[offset:offset + blockSize]
            offset += blockSize

        return bytearray(result)