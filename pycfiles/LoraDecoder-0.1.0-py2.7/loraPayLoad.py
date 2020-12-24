# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/loradecoder/loraPayLoad.py
# Compiled at: 2016-06-20 07:00:28
from collections import OrderedDict
import struct, binascii
from loradecoder.loraExceptions import loraPayloadException

class loraPayLoad:
    payLoadFormat = OrderedDict()
    numBytesPayload = 0
    payLoadData = None

    def __init__(self, format=None):
        if not format == None:
            if isinstance(ele, dict):
                payLoadFormat = format
        return

    def getNumbytes(self):
        return self.numBytesPayload

    def setPayload(self, p):
        if len(p) == self.numBytesPayload * 2:
            self.payLoadData = p
        elif len(p) >= self.numBytesPayload * 2:
            self.payLoadData = p
        else:
            self.payLoadData = None
            raise loraPayloadException('ERROR: payload data smaller (' + str(len(p)) + ' bytes) than format (' + str(self.numBytesPayload * 2) + ' bytes)')
        return

    def getValue(self, meaning):
        if meaning in self.payLoadFormat:
            s = self.payLoadFormat[meaning]['startFrom'] * 2
            e = s + self.payLoadFormat[meaning]['numBytes'] * 2
            data = self.payLoadData[s:e]
            if self.payLoadFormat[meaning]['type'] == 'INT':
                return int(data, 16)
            if self.payLoadFormat[meaning]['type'] == 'STRING':
                return data.decode('hex')
            if self.payLoadFormat[meaning]['type'] == 'FLOAT':
                return struct.unpack('!f', binascii.unhexlify(data))[0]
            raise loraPayloadException('Warning: incompatible type format for loraPayLoad')
        else:
            raise loraPayloadException('Warning: meaning ' + meaning + ' for payload data is not defined')

    def addItem(self, MEANING, NUMBYTES=1, REPRESENTATION='INT'):
        if REPRESENTATION is 'FLOAT':
            if NUMBYTES < 4:
                raise loraPayloadException('Warning: for FLOAT type a minimum bytes of 2 is required')
        self.payLoadFormat[MEANING] = {'numBytes': NUMBYTES, 'type': REPRESENTATION, 'startFrom': self.numBytesPayload}
        self.numBytesPayload = self.numBytesPayload + NUMBYTES

    def printFormat(self):
        output = ''
        output += '| LoraPacket payload format'
        output += '| meaning | number of bytes | type | startposition'
        for key, value in self.payLoadFormat.items():
            output += ('| {} : {} : {} : {}').format(key, str(value['numBytes']), str(value['type']), str(value['startFrom']))

        return output

    def printValues(self):
        output = '| LoraPacket payload'
        output += '|-------------------'
        output += ('| {:<20} {:<20} {:<10} {:<20} {:<10}').format('meaning', 'number of bytes', 'type', 'startposition', 'data')
        for key, value in self.payLoadFormat.items():
            output += ('| {:<20} {:<20} {:<10} {:<20} {:<10}').format(key, str(value['numBytes']), str(value['type']), str(value['startFrom']), self.getValue(key))

        return output

    def getPayload(self):
        if not self.payLoadData == None:
            dataArray = {}
            for key, value in self.payLoadFormat.items():
                dataArray[key] = self.getValue(key)

            return dataArray
        return
        return