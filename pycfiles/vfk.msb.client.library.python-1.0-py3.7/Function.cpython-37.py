# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/Function.py
# Compiled at: 2018-08-16 06:12:08
# Size of source mod 2**32: 1661 bytes
"""
Copyright (c) 2017
Fraunhofer Institute for Manufacturing Engineering
and Automation (IPA)
Author: Daniel Stock
mailto: daniel DOT stock AT ipa DOT fraunhofer DOT com
See the file "LICENSE" for the full license governing this code.
"""
from msb_client.DataFormat import *
from msb_client.ComplexDataFormat import *
import json, copy

class Function:

    def __init__(self, functionId, function_name, function_description, function_dataformat, fnpointer=None, isArray=False, responseEvents=None):
        self.functionId = functionId
        self.name = function_name
        self.description = function_description
        self.isArray = isArray
        if isinstance(function_dataformat, DataFormat) or isinstance(function_dataformat, ComplexDataFormat):
            self.dataFormat = copy.deepcopy(function_dataformat).getDataFormat()
        else:
            if type(function_dataformat) == type(datetime):
                self.dataFormat = DataFormat(function_dataformat, isArray).getDataFormat()
            else:
                if function_dataformat is None:
                    self.dataFormat = None
                else:
                    try:
                        json_object = {'dataObject': json.loads(function_dataformat)}
                        self.dataFormat = json_object
                    except:
                        self.dataFormat = DataFormat(function_dataformat, isArray).getDataFormat()

                    if responseEvents is None:
                        self.responseEvents = []
                    else:
                        self.responseEvents = responseEvents
                    self.implementation = fnpointer