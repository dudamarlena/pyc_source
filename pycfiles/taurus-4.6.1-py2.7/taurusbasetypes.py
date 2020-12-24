# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusbasetypes.py
# Compiled at: 2019-08-19 15:09:29
"""
a misc collection of basic types
"""
import datetime
from .util.enumeration import Enumeration
from .util.log import taurus4_deprecation
from enum import IntEnum
from future.utils import PY2
from builtins import object
__all__ = [
 'TaurusSWDevState', 'TaurusSWDevHealth', 'OperationMode',
 'TaurusSerializationMode', 'SubscriptionState', 'TaurusEventType',
 'MatchLevel', 'TaurusElementType', 'LockStatus', 'DataFormat',
 'AttrQuality', 'AttrAccess', 'DisplayLevel', 'ManagerState',
 'TaurusTimeVal', 'TaurusAttrValue', 'TaurusConfigValue', 'DataType',
 'TaurusLockInfo', 'TaurusDevState', 'TaurusModelValue']
__docformat__ = 'restructuredtext'

class TaurusDevState(IntEnum):
    """Enumeration of possible states of :class:`taurus.core.TaurusDevice`
    objects. This is returned, e.g. by :meth:`TaurusDevice.state`.

    The description of the values of this enumeration is:

    - Ready: the device can be operated by the user and could even be
      involved in some operation.
    - NotReady: the device can not be operated by the user (e.g. due to
      still being initialized, or due to a device failure,...)
    - Undefined: it is not possible to retrieve a coherent state from the
      device (e.g. due to communication, or to contradictory internal
      states, ...)
    """
    Ready = 1
    NotReady = 2
    Undefined = 4


OperationMode = Enumeration('OperationMode', ('OFFLINE', 'ONLINE'))
TaurusSerializationMode = Enumeration('TaurusSerializationMode', ('Serial', 'Concurrent',
                                                                  'TangoSerial'))
TaurusEventType = Enumeration('TaurusEventType', ('Change', 'Config', 'Periodic', 'Error'))
MatchLevel = Enumeration('MatchLevel', ('ANY', 'SHORT', 'NORMAL', 'COMPLETE', 'SHORT_NORMAL',
                                        'NORMAL_COMPLETE'))
TaurusElementType = Enumeration('TaurusElementType', ('Unknown', 'Name', 'DeviceClass',
                                                      'Device', 'DeviceAlias', 'Domain',
                                                      'Family', 'Member', 'Server',
                                                      'ServerName', 'ServerInstance',
                                                      'Exported', 'Host', 'Attribute',
                                                      'AttributeAlias', 'Command',
                                                      'Property', 'Configuration',
                                                      'Authority'))
LockStatus = Enumeration('LockStatus', ('Unlocked', 'Locked', 'LockedMaster', 'Unknown'))
DataFormat = Enumeration('DataFormat', ('_0D', '_1D', '_2D'))
DataType = Enumeration('DataType', ('Integer', 'Float', 'String', 'Boolean', 'Bytes',
                                    'DevState', 'DevEncoded', 'Object'))
__PYTHON_TYPE_TO_TAURUS_DATATYPE = {str: DataType.String, 
   int: DataType.Integer, 
   float: DataType.Float, 
   bool: DataType.Boolean}
if PY2:
    __PYTHON_TYPE_TO_TAURUS_DATATYPE[long] = DataType.Integer
else:
    __PYTHON_TYPE_TO_TAURUS_DATATYPE[bytes] = DataType.Bytes
DataType.from_python_type = __PYTHON_TYPE_TO_TAURUS_DATATYPE.get
SubscriptionState = Enumeration('SubscriptionState', ('Unsubscribed', 'Subscribing',
                                                      'Subscribed', 'PendingSubscribe'))

class AttrQuality(IntEnum):
    """Enumeration of quality states for Taurus attributes. based on
    This is the Taurus equivalent to PyTango.AttrQuality.
    The members present in PyTango are also defined here with the same values,
    allowing equality comparisons with :class:`PyTango.AttrQuality` (but not
    identity checks!)::

        from taurus.core import AttrQuality as Q1
        from PyTango import AttrQuality as Q2

        Q1.ATTR_ALARM == Q2.ATTR_ALARM                  # --> True
        Q1.ATTR_ALARM in (Q2.ATTR_ALARM, Q2.ATTR_ALARM) # --> True
        Q1.ATTR_ALARM == 2                              # --> True
        Q1.ATTR_ALARM is 2                              # --> False
        Q1.ATTR_ALARM is Q2.ATTR_ALARM                  # --> False
    """
    ATTR_VALID = 0
    ATTR_INVALID = 1
    ATTR_ALARM = 2
    ATTR_CHANGING = 3
    ATTR_WARNING = 4

    def __str__(self):
        return self.name


AttrAccess = Enumeration('AttrAccess', ('READ', 'READ_WITH_WRITE', 'WRITE', 'READ_WRITE'))
DisplayLevel = Enumeration('DisplayLevel', ('OPERATOR', 'EXPERT', 'DEVELOPER'))
ManagerState = Enumeration('ManagerState', ('UNINITIALIZED', 'INITED', 'CLEANED'))

class DeprecatedEnum(object):

    def __init__(self, name, alt):
        self.__name = name
        self.__alt = alt

    def __getattr__(self, name):
        raise RuntimeError('%s enumeration was removed. Use %s instead' % (
         self.__name, self.__alt))


TaurusSWDevState = DeprecatedEnum('TaurusSWDevState', 'TaurusDevState')
TaurusSWDevHealth = DeprecatedEnum('TaurusSWDevHealth', 'TaurusDevState')

class TaurusTimeVal(object):

    def __init__(self):
        self.tv_sec = 0
        self.tv_usec = 0
        self.tv_nsec = 0

    def __repr__(self):
        return '%s(tv_sec=%i, tv_usec=%i, tv_nsec=%i)' % (self.__class__.__name__, self.tv_sec, self.tv_usec, self.tv_nsec)

    def __float__(self):
        return self.totime()

    def totime(self):
        return self.tv_nsec * 1e-09 + self.tv_usec * 1e-06 + self.tv_sec

    def todatetime(self):
        return datetime.datetime.fromtimestamp(self.totime())

    def isoformat(self):
        return self.todatetime().isoformat()

    @staticmethod
    def fromtimestamp(v):
        tv = TaurusTimeVal()
        tv.tv_sec = int(v)
        usec = (v - tv.tv_sec) * 1000000
        tv.tv_usec = int(usec)
        tv.tv_nsec = int((usec - tv.tv_usec) * 1000)
        return tv

    @staticmethod
    def fromdatetime(v):
        import time
        tv = TaurusTimeVal()
        tv.tv_sec = int(time.mktime(v.timetuple()))
        tv.tv_usec = v.microsecond
        tv.tv_nsec = 0
        return tv

    @staticmethod
    def now():
        return TaurusTimeVal.fromdatetime(datetime.datetime.now())


class TaurusModelValue(object):

    def __init__(self):
        self.rvalue = None
        return

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, repr(self.__dict__))


class TaurusAttrValue(TaurusModelValue):

    def __init__(self):
        TaurusModelValue.__init__(self)
        self.wvalue = None
        self.time = None
        self.quality = AttrQuality.ATTR_VALID
        self.error = None
        return


class TaurusConfigValue(object):

    @taurus4_deprecation(alt='TaurusAttrValue')
    def __init__(self):
        pass


class TaurusLockInfo(object):
    LOCK_STATUS_UNKNOWN = 'Lock status unknown'

    def __init__(self):
        self.status = LockStatus.Unknown
        self.status_msg = self.LOCK_STATUS_UNKNOWN
        self.id = None
        self.host = None
        self.klass = None
        return

    def __repr__(self):
        return self.status_msg