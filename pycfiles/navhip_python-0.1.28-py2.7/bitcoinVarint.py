# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/bitcoinVarint.py
# Compiled at: 2020-02-12 12:44:00
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
from .navhipException import BTChipException

def readVarint(buffer, offset):
    varintSize = 0
    value = 0
    if buffer[offset] < 253:
        value = buffer[offset]
        varintSize = 1
    elif buffer[offset] == 253:
        value = buffer[(offset + 2)] << 8 | buffer[(offset + 1)]
        varintSize = 3
    elif buffer[offset] == 254:
        value = buffer[(offset + 4)] << 24 | buffer[(offset + 3)] << 16 | buffer[(offset + 2)] << 8 | buffer[(offset + 1)]
        varintSize = 5
    else:
        raise BTChipException('unsupported varint')
    return {'value': value, 'size': varintSize}


def writeVarint(value, buffer):
    if value < 253:
        buffer.append(value)
    elif value <= 65535:
        buffer.append(253)
        buffer.append(value & 255)
        buffer.append(value >> 8 & 255)
    elif value <= 4294967295:
        buffer.append(254)
        buffer.append(value & 255)
        buffer.append(value >> 8 & 255)
        buffer.append(value >> 16 & 255)
        buffer.append(value >> 24 & 255)
    else:
        raise BTChipException('unsupported encoding')
    return buffer


def getVarintSize(value):
    if value < 253:
        return 1
    if value <= 65535:
        return 3
    if value <= 4294967295:
        return 5
    raise BTChipException('unsupported encoding')