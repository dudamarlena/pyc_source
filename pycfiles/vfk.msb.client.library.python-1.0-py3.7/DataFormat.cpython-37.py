# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/DataFormat.py
# Compiled at: 2018-08-16 06:12:07
# Size of source mod 2**32: 847 bytes
"""
Copyright (c) 2017
Fraunhofer Institute for Manufacturing Engineering
and Automation (IPA)
Author: Daniel Stock
mailto: daniel DOT stock AT ipa DOT fraunhofer DOT com
See the file "LICENSE" for the full license governing this code.
"""
from msb_client.DataType import *

class DataFormat:

    def __init__(self, dataType=None, isArray=None):
        self.isArray = isArray
        dataFormat = {}
        dataObject = {}
        if isArray != None and isArray:
            dataObject['type'] = 'array'
            dataObject['items'] = getDataType(dataType)
            dataFormat['dataObject'] = dataObject
        else:
            dataObject = getDataType(dataType)
            dataFormat['dataObject'] = dataObject
        self.dataFormat = dataFormat

    def getDataFormat(self):
        return self.dataFormat