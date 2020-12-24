# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/ComplexDataFormat.py
# Compiled at: 2018-08-16 06:12:08
# Size of source mod 2**32: 4201 bytes
"""
Copyright (c) 2017
Fraunhofer Institute for Manufacturing Engineering
and Automation (IPA)
Author: Daniel Stock
mailto: daniel DOT stock AT ipa DOT fraunhofer DOT com
See the file "LICENSE" for the full license governing this code.
"""
from msb_client.DataType import *

class ComplexDataFormat:

    def __init__(self, objectName):
        self.objectName = objectName
        dataFormat = {}
        dataFormat[objectName] = {}
        dataFormat['dataObject'] = {}
        dataFormat[objectName]['type'] = 'object'
        dataFormat['dataObject']['$ref'] = '#/definitions/' + self.objectName
        self.dataFormat = dataFormat

    objectName = ''

    def getDataFormat(self):
        return self.dataFormat

    def addProperty(self, propertyName, dataType, isArray=None):
        if isArray != None and isArray:
            if 'properties' not in self.dataFormat[self.objectName].keys():
                self.dataFormat[self.objectName]['properties'] = {}
            if isinstance(dataType, ComplexDataFormat):
                dt = dataType.getDataFormat()[dataType.objectName]
                if dt != {}:
                    self.dataFormat[self.objectName]['properties'][propertyName] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName]['items'] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName]['type'] = 'array'
                    self.dataFormat[self.objectName]['properties'][propertyName]['items']['$ref'] = '#/definitions/' + dataType.objectName
                    self.dataFormat[dataType.objectName] = dt
            else:
                dt = getDataType(dataType)
            if dt != {}:
                if 'properties' in self.dataFormat[self.objectName].keys():
                    self.dataFormat[self.objectName]['properties'][propertyName] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName]['type'] = 'array'
                    self.dataFormat[self.objectName]['properties'][propertyName]['items'] = dt
                else:
                    self.dataFormat[self.objectName]['properties'] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName]['type'] = 'array'
                    self.dataFormat[self.objectName]['properties'][propertyName]['items'] = dt
        else:
            if 'properties' not in self.dataFormat[self.objectName].keys():
                self.dataFormat[self.objectName]['properties'] = {}
        if isinstance(dataType, ComplexDataFormat):
            self.dataFormat[dataType.objectName] = {}
            dt = dataType.getDataFormat()[dataType.objectName]
            if dt != {}:
                self.dataFormat[self.objectName]['properties'][propertyName] = {}
                self.dataFormat[self.objectName]['properties'][propertyName]['$ref'] = '#/definitions/' + dataType.objectName
                self.dataFormat[dataType.objectName] = dt
        else:
            dt = getDataType(dataType)
            if dt != {}:
                if 'properties' in self.dataFormat[self.objectName].keys():
                    self.dataFormat[self.objectName]['properties'][propertyName] = dt
                else:
                    self.dataFormat[self.objectName]['properties'] = {}
                    self.dataFormat[self.objectName]['properties'][propertyName] = dt