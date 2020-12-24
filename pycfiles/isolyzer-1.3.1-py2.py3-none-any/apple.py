# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/isolyzer/isolyzer/apple.py
# Compiled at: 2018-01-26 07:48:08
"""Parser functions for Apple file systems"""
import xml.etree.ElementTree as ET
from . import byteconv as bc
from . import shared

def parseZeroBlock(bytesData):
    """Parse Zero Block and return extracted properties"""
    properties = ET.Element('appleZeroBlock')
    shared.addProperty(properties, 'signature', bc.bytesToText(bytesData[0:2]))
    shared.addProperty(properties, 'blockSize', bc.bytesToUShortInt(bytesData[2:4]))
    shared.addProperty(properties, 'blockCount', bc.bytesToUInt(bytesData[4:8]))
    shared.addProperty(properties, 'deviceType', bc.bytesToUShortInt(bytesData[8:10]))
    shared.addProperty(properties, 'deviceID', bc.bytesToUShortInt(bytesData[10:12]))
    shared.addProperty(properties, 'driverData', bc.bytesToUInt(bytesData[12:16]))
    shared.addProperty(properties, 'driverDescriptorCount', bc.bytesToUShortInt(bytesData[80:82]))
    shared.addProperty(properties, 'driverDescriptorBlockStart', bc.bytesToUInt(bytesData[82:86]))
    shared.addProperty(properties, 'driverDescriptorBlockCount', bc.bytesToUShortInt(bytesData[86:88]))
    shared.addProperty(properties, 'driverDescriptorSystemType', bc.bytesToUShortInt(bytesData[88:90]))
    return properties


def parsePartitionMap(bytesData):
    """Parse Partition Map and return extracted properties"""
    properties = ET.Element('applePartitionMap')
    shared.addProperty(properties, 'signature', bc.bytesToText(bytesData[0:2]))
    shared.addProperty(properties, 'numberOfPartitionEntries', bc.bytesToUInt(bytesData[4:8]))
    shared.addProperty(properties, 'partitionBlockStart', bc.bytesToUInt(bytesData[8:12]))
    shared.addProperty(properties, 'partitionBlockCount', bc.bytesToUInt(bytesData[12:16]))
    shared.addProperty(properties, 'partitionName', bc.bytesToText(bytesData[16:48]))
    shared.addProperty(properties, 'partitionType', bc.bytesToText(bytesData[48:80]))
    shared.addProperty(properties, 'partitionLogicalBlockStart', bc.bytesToUInt(bytesData[80:84]))
    shared.addProperty(properties, 'partitionLogicalBlockCount', bc.bytesToUInt(bytesData[84:88]))
    shared.addProperty(properties, 'partitionFlags', bc.bytesToUInt(bytesData[88:92]))
    shared.addProperty(properties, 'bootCodeBlockStart', bc.bytesToUInt(bytesData[92:96]))
    shared.addProperty(properties, 'bootCodeSizeInBytes', bc.bytesToUInt(bytesData[96:100]))
    shared.addProperty(properties, 'bootCodeLoadAddress', bc.bytesToUInt(bytesData[100:104]))
    shared.addProperty(properties, 'bootCodeJumpAddress', bc.bytesToUInt(bytesData[108:112]))
    shared.addProperty(properties, 'bootCodeChecksum', bc.bytesToUInt(bytesData[116:120]))
    shared.addProperty(properties, 'processorType', bc.bytesToText(bytesData[120:136]))
    return properties


def parseMasterDirectoryBlock(bytesData):
    """Parse Master Directory Block and return extracted properties"""
    properties = ET.Element('masterDirectoryBlock')
    shared.addProperty(properties, 'signature', bc.bytesToText(bytesData[0:2]))
    shared.addProperty(properties, 'blockSize', bc.bytesToUShortInt(bytesData[18:20]))
    shared.addProperty(properties, 'blockCount', bc.bytesToUInt(bytesData[20:24]))
    charsVolumeName = bc.bytesToUnsignedChar(bytesData[36:37])
    shared.addProperty(properties, 'volumeName', bc.bytesToText(bytesData[37:37 + charsVolumeName]))
    return properties


def parseHFSPlusVolumeHeader(bytesData):
    """Parse HFS Plus Volume header and return extracted properties"""
    properties = ET.Element('hfsPlusVolumeheader')
    shared.addProperty(properties, 'signature', bc.bytesToText(bytesData[0:2]))
    shared.addProperty(properties, 'version', bc.bytesToUShortInt(bytesData[2:4]))
    shared.addProperty(properties, 'blockSize', bc.bytesToUInt(bytesData[40:44]))
    shared.addProperty(properties, 'blockCount', bc.bytesToUInt(bytesData[44:48]))
    return properties