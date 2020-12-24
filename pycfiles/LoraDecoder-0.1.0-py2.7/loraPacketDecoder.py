# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/loradecoder/loraPacketDecoder.py
# Compiled at: 2016-06-20 07:00:28
import xml.etree.ElementTree as ET, struct
from datetime import datetime
from loradecoder.loraPayLoad import loraPayLoad
from loradecoder.loraExceptions import loraPayloadException
from loradecoder.loraExceptions import loraDecoderException

class loraPacketDecoder:
    rawData = ''
    dataFormat = None
    dataArray = {}

    def __init__(self, rawData, dataFormat=None):
        if isinstance(dataFormat, loraPayLoad):
            self.dataFormat = dataFormat
        self.rawData = rawData
        self.processRawData()

    def processRawData(self):
        try:
            startData = self.rawData.find('<?xml version="1.0"')
            if startData < 0:
                return
            self.rawData = self.rawData[startData:]
            realData = ET.fromstring(self.rawData)
            for item in realData:
                s = item.tag.find('}')
                name = item.tag[s + 1:]
                self.dataArray[name] = item.text

            if isinstance(self.dataFormat, loraPayLoad):
                self.dataFormat.setPayload(self.getPayloadRaw())
        except Exception:
            raise loraDecoderException('Incorrect raw data supplied')

    def getTime(self):
        try:
            time = self.dataArray['Time'][0:19]
            return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            loraDecoderException('Error in datetime inside of the loraPacket: ' + ValueError)

    def setFormat(self, dataFormat):
        if isinstance(dataFormat, loraPayLoad):
            self.dataFormat = dataFormat
            self.dataFormat.setPayload(self.getPayloadRaw())
        else:
            loraDecoderException('Supplied lora format is not of class loraPayload')

    def getFormat(self):
        return self.dataFormat

    def getLatitude(self):
        return float(self.dataArray['LrrLAT'])

    def getLongtitude(self):
        return float(self.dataArray['LrrLON'])

    def getUID(self):
        return str(self.dataArray['DevEUI'])

    def getPayloadRaw(self):
        return str(self.dataArray['payload_hex'])

    def getPayloadValue(self, meaning):
        if not isinstance(self.dataFormat, loraPayLoad):
            raise loraDecoderException('No dataformat supplied to lora packet decoder')
        return self.dataFormat.getValue(meaning)

    def getPayloadBytes(self):
        return self.dataFormat.getNumbytes()

    def getPayloadItems(self):
        return self.dataFormat.getPayload()

    def printPayload(self):
        return self.dataFormat.printValues()

    def getCustomerID(self):
        return str(self.dataArray['CustomerID'])

    def getCustomerData(self):
        return str(self.dataArray['CustomerData'])

    def getRSSI(self):
        return float(self.dataArray['LrrRSSI'])

    def getSNR(self):
        return float(self.dataArray['LrrSNR'])

    def getPort(self):
        return float(self.dataArray['FPort'])

    def getLoraGatewayID(self):
        return str(self.dataArray['Lrrid'])

    def getLoraGatewayID(self):
        return str(self.dataArray['Lrcid'])

    def get(self, varName):
        try:
            return self.dataArray[varName]
        except:
            return

        return

    def getPayloadDataHex(self, startByte=0, numBytes=1):
        return self.dataArray['payload_hex'][startByte:numBytes * 2]

    def getPayloadDataInt(self, startByte=0, numBytes=1):
        return int(self.dataArray['payload_hex'][startByte:numBytes * 2], 16)

    def getPayloadDataString(self, startByte=0, numBytes=1):
        return self.dataArray['payload_hex'][startByte:numBytes * 2].decode('hex')

    def getPayloadDataFloat(self, startByte=0, numBytes=1):
        return struct.unpack('!f', self.dataArray['payload_hex'][startByte:numBytes * 2])[0]