# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/enums.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains all basic tango enumerations"""
__all__ = [
 'TangoObjectType', 'EVENT_TO_POLLING_EXCEPTIONS',
 'FROM_TANGO_TO_NUMPY_TYPE', 'FROM_TANGO_TO_STR_TYPE', 'DevState']
__docformat__ = 'restructuredtext'
from taurus.core.util.enumeration import Enumeration
from enum import IntEnum
TangoObjectType = Enumeration('TangoObjectType', [
 'Authority', 'Server', 'Class', 'Device',
 'Attribute', 'Property', 'Configuration',
 'Object'])
TangoObjectType.Database = TangoObjectType.Authority
import numpy, PyTango
EVENT_TO_POLLING_EXCEPTIONS = ('API_AttributePollingNotStarted', 'API_DSFailedRegisteringEvent',
                               'API_NotificationServiceFailed', 'API_EventChannelNotExported',
                               'API_EventTimeout', 'API_EventPropertiesNotSet', 'API_CommandNotFound',
                               'API_PollObjNotFound')
FROM_TANGO_TO_NUMPY_TYPE = {PyTango.DevVoid: None, 
   PyTango.DevBoolean: numpy.bool8, 
   PyTango.DevUChar: numpy.uint8, 
   PyTango.DevShort: numpy.short, 
   PyTango.DevUShort: numpy.ushort, 
   PyTango.DevLong: numpy.int32, 
   PyTango.DevULong: numpy.uint32, 
   PyTango.DevLong64: numpy.int64, 
   PyTango.DevULong64: numpy.uint64, 
   PyTango.DevString: numpy.str, 
   PyTango.DevDouble: numpy.float64, 
   PyTango.DevFloat: numpy.float32}
FROM_TANGO_TO_STR_TYPE = {PyTango.DevVoid: None, 
   PyTango.DevBoolean: 'bool8', 
   PyTango.DevUChar: 'uint8', 
   PyTango.DevShort: 'short', 
   PyTango.DevUShort: 'ushort', 
   PyTango.DevLong: 'int32', 
   PyTango.DevULong: 'uint32', 
   PyTango.DevLong64: 'int64', 
   PyTango.DevULong64: 'uint64', 
   PyTango.DevString: 'str', 
   PyTango.DevDouble: 'float64', 
   PyTango.DevFloat: 'float32'}

class DevState(IntEnum):
    """ This is the taurus.core.tango equivalent to PyTango.DevState.
    It defines the same members and uses the same numerical values internally,
    allowing equality comparisons with :class:`PyTango.DevState` (but not
    identity checks!)::

        from taurus.core.tango import DevState as D1
        from PyTango import DevState as D2

        D1.OPEN == D2.OPEN          # --> True
        D1.OPEN in (D2.ON, D2.OPEN) # --> True
        D1.OPEN == 3                # --> True
        D1.OPEN is 3                # --> False
        D1.OPEN is D2.OPEN          # --> False

     """
    ON = 0
    OFF = 1
    CLOSE = 2
    OPEN = 3
    INSERT = 4
    EXTRACT = 5
    MOVING = 6
    STANDBY = 7
    FAULT = 8
    INIT = 9
    RUNNING = 10
    ALARM = 11
    DISABLE = 12
    UNKNOWN = 13