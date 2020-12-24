# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/navhipHelpers.py
# Compiled at: 2020-02-12 12:19:44
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
import decimal, re
SATOSHI_PER_COIN = decimal.Decimal(100000000.0)
COIN_PER_SATOSHI = decimal.Decimal(1) / SATOSHI_PER_COIN

def satoshi_to_btc(satoshi_count):
    if satoshi_count == 0:
        return decimal.Decimal(0)
    r = satoshi_count * COIN_PER_SATOSHI
    return r.normalize()


def btc_to_satoshi(btc):
    return int(decimal.Decimal(btc) * SATOSHI_PER_COIN)


def writeUint32BE(value, buffer):
    buffer.append(value >> 24 & 255)
    buffer.append(value >> 16 & 255)
    buffer.append(value >> 8 & 255)
    buffer.append(value & 255)
    return buffer


def writeUint32LE(value, buffer):
    buffer.append(value & 255)
    buffer.append(value >> 8 & 255)
    buffer.append(value >> 16 & 255)
    buffer.append(value >> 24 & 255)
    return buffer


def writeHexAmount(value, buffer):
    buffer.append(value & 255)
    buffer.append(value >> 8 & 255)
    buffer.append(value >> 16 & 255)
    buffer.append(value >> 24 & 255)
    buffer.append(value >> 32 & 255)
    buffer.append(value >> 40 & 255)
    buffer.append(value >> 48 & 255)
    buffer.append(value >> 56 & 255)
    return buffer


def writeHexAmountBE(value, buffer):
    buffer.append(value >> 56 & 255)
    buffer.append(value >> 48 & 255)
    buffer.append(value >> 40 & 255)
    buffer.append(value >> 32 & 255)
    buffer.append(value >> 24 & 255)
    buffer.append(value >> 16 & 255)
    buffer.append(value >> 8 & 255)
    buffer.append(value & 255)
    return buffer


def parse_bip32_path(path):
    if len(path) == 0:
        return bytearray([0])
    result = []
    elements = path.split('/')
    if len(elements) > 10:
        raise BTChipException('Path too long')
    for pathElement in elements:
        element = re.split("'|h|H", pathElement)
        if len(element) == 1:
            writeUint32BE(int(element[0]), result)
        else:
            writeUint32BE(2147483648 | int(element[0]), result)

    return bytearray([len(elements)] + result)