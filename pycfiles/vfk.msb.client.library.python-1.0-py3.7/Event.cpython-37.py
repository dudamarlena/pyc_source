# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/Event.py
# Compiled at: 2018-08-16 06:12:07
# Size of source mod 2**32: 1766 bytes
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

class Event:

    def __init__(self, eventId, event_name, event_description, event_dataFormat, priority=0, isArray=False):
        self.eventId = eventId
        self.name = event_name
        self.description = event_description
        if isinstance(event_dataFormat, DataFormat) or isinstance(event_dataFormat, ComplexDataFormat):
            self.dataFormat = copy.deepcopy(event_dataFormat).getDataFormat()
            self.df = event_dataFormat
        else:
            if isinstance(event_dataFormat, DataType):
                self.dataFormat = DataFormat(event_dataFormat, isArray).getDataFormat()
                self.df = convertDataType(event_dataFormat)
            else:
                if type(event_dataFormat) == type(datetime):
                    self.dataFormat = DataFormat(event_dataFormat, isArray).getDataFormat()
                    self.df = datetime.datetime
                else:
                    if event_dataFormat is None:
                        self.dataFormat = None
                        self.df = None
                    else:
                        try:
                            json_object = {'dataObject': json.loads(event_dataFormat)}
                            self.dataFormat = json_object
                        except:
                            self.dataFormat = DataFormat(event_dataFormat, isArray).getDataFormat()

                        self.df = event_dataFormat
        self.priority = priority
        self.isArray = isArray

    id = 0
    dataObject = 0