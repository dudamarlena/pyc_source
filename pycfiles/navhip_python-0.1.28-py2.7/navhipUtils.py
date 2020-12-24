# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/navhipUtils.py
# Compiled at: 2020-02-12 12:44:48
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
from .navhipException import *
from .bitcoinTransaction import *
from .navhipHelpers import *

def compress_public_key(publicKey):
    if publicKey[0] == 4:
        if publicKey[64] & 1 != 0:
            prefix = 3
        else:
            prefix = 2
        result = [
         prefix]
        result.extend(publicKey[1:33])
        return bytearray(result)
    if publicKey[0] == 3 or publicKey[0] == 2:
        return publicKey
    raise BTChipException('Invalid public key format')


def format_transaction(dongleOutputData, trustedInputsAndInputScripts, version=3, time=0, lockTime=0, strdzel=[]):
    transaction = bitcoinTransaction()
    transaction.version = []
    writeUint32LE(version, transaction.version)
    transaction.time = []
    writeUint32LE(time, transaction.time)
    for item in trustedInputsAndInputScripts:
        newInput = bitcoinInput()
        newInput.prevOut = item[0][4:40]
        newInput.script = item[1]
        if len(item) > 2:
            newInput.sequence = bytearray(item[2].decode('hex'))
        else:
            newInput.sequence = bytearray([255, 255, 255, 255])
        transaction.inputs.append(newInput)

    result = transaction.serialize(True)
    result.extend(dongleOutputData)
    writeUint32LE(lockTime, result)
    writeUint32LE(len(strdzeel), result)
    result.extend(strdzeel)
    return bytearray(result)


def get_regular_input_script(sigHashtype, publicKey):
    if len(sigHashtype) >= 76:
        raise BTChipException('Invalid sigHashtype')
    if len(publicKey) >= 76:
        raise BTChipException('Invalid publicKey')
    result = [
     len(sigHashtype)]
    result.extend(sigHashtype)
    result.append(len(publicKey))
    result.extend(publicKey)
    return bytearray(result)


def write_pushed_data_size(data, buffer):
    if len(data) > 65535:
        raise BTChipException('unsupported encoding')
    if len(data) < 76:
        buffer.append(len(data))
    elif len(data) > 255:
        buffer.append(77)
        buffer.append(len(data) & 255)
        buffer.append(len(data) >> 8 & 255)
    else:
        buffer.append(76)
        buffer.append(len(data))
    return buffer


def get_p2sh_input_script(redeemScript, sigHashtypeList):
    result = [
     0]
    for sigHashtype in sigHashtypeList:
        write_pushed_data_size(sigHashtype, result)
        result.extend(sigHashtype)

    write_pushed_data_size(redeemScript, result)
    result.extend(redeemScript)
    return bytearray(result)


def get_p2pk_input_script(sigHashtype):
    if len(sigHashtype) >= 76:
        raise BTChipException('Invalid sigHashtype')
    result = [
     len(sigHashtype)]
    result.extend(sigHashtype)
    return bytearray(result)


def get_output_script(amountScriptArray):
    result = [
     len(amountScriptArray)]
    for amountScript in amountScriptArray:
        writeHexAmount(btc_to_satoshi(str(amountScript[0])), result)
        writeVarint(len(amountScript[1]), result)
        result.extend(amountScript[1])

    return bytearray(result)