# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/ses2.py
# Compiled at: 2013-11-20 18:11:42
from fcntl import ioctl
from ctypes import *
import struct, platform
IOC_VOID = 536870912
IOCPARM_SHIFT = 13
IOCPARM_MASK = (1 << IOCPARM_SHIFT) - 1

def _IOC(inout, group, num, length):
    return inout | (length & IOCPARM_MASK) << 16 | group << 8 | num


def _IO(g, n):
    return _IOC(IOC_VOID, g, n, 0)


SESIOC = ord('s') - 32
SESIOC_GETNOBJ = _IO(SESIOC, 1)
SESIOC_GETOBJMAP = _IO(SESIOC, 2)
SESIOC_GETENCSTAT = _IO(SESIOC, 3)
SESIOC_SETENCSTAT = _IO(SESIOC, 4)
SESIOC_GETOBJSTAT = _IO(SESIOC, 5)
SESIOC_SETOBJSTAT = _IO(SESIOC, 6)
SESIOC_GETTEXT = _IO(SESIOC, 7)
SESIOC_INIT = _IO(SESIOC, 8)
OBJSTAT = {0: 'UNSUPPORTED', 
   1: 'OK', 
   2: 'CRITICAL', 
   3: 'NONCRITICAL', 
   4: 'UNRECOVERABLE', 
   5: 'NOTINSTALLED', 
   6: 'UNKNOWN', 
   7: 'UNAVAILABLE'}
SESTYP = {0: 'UNSPECIFIED', 
   1: 'DEVICE', 
   2: 'POWER', 
   3: 'FAN', 
   4: 'THERM', 
   5: 'DOORLOCK', 
   6: 'ALARM', 
   7: 'ESCC', 
   8: 'SCC', 
   9: 'NVRAM', 
   11: 'UPS', 
   12: 'DISPLAY', 
   13: 'KEYPAD', 
   14: 'ENCLOSURE', 
   15: 'SCSIXVR', 
   16: 'LANGUAGE', 
   17: 'COMPORT', 
   18: 'VOM', 
   19: 'AMMETER', 
   20: 'SCSI_TGT', 
   21: 'SCSI_INI', 
   22: 'SUBENC', 
   23: 'ARRAY', 
   24: 'SASEXPANDER', 
   25: 'SASCONNECTOR'}
ENCSTAT = {0: 'OK', 
   1: 'UNRECOVERABLE', 
   2: 'CRITICAL', 
   4: 'NONCRITICAL', 
   8: 'INFO'}

class Object(object):
    """SES2 object - represents things like array slots, fans, sensors, power supplies, etc"""

    def __init__(self, data, sesdev):
        self.obj_id, self.subencid, self.object_type = data
        self.sesdev = sesdev

    @property
    def type(self):
        """the type of ses object (ARRAY, FAN, etc)"""
        return SESTYP[self.object_type]

    def __str__(self):
        return '<%-12s %2d %2d (0x%02x 0x%02x 0x%02x 0x%02x)>' % (
         self.type,
         self.obj_id,
         self.subencid,
         self.statdata[0],
         self.statdata[1],
         self.statdata[2],
         self.statdata[3])

    def updatestatus(self):
        """refresh all of this object's status information"""
        self.statdata = self.sesdev.getobjstat(self.obj_id)[1:]

    @property
    def status(self):
        """general ses object status - returns array of statuses"""
        return OBJSTAT[(self.statdata[0] & 15)]

    @property
    def ident(self):
        return not self.statdata[2] & 2 == 0

    @ident.setter
    def ident(self, value=True):
        """control the led indicator on an object (currently only ARRAY objects)"""
        if self.type == 'ARRAY':
            if value == 'toggle':
                self.updatestatus()
                self.sesdev.setobjstat(self.obj_id, (128, 0, self.statdata[2] ^ 2, 0))
            elif value:
                self.sesdev.setobjstat(self.obj_id, (128, 0, 2, 0))
            else:
                self.sesdev.setobjstat(self.obj_id, (128, 0, 0, 0))
        else:
            return False
        self.updatestatus()
        return True

    @property
    def fanrpm(self):
        """speed of a FAN element in RPM"""
        if self.type != 'FAN':
            return None
        else:
            return ((self.statdata[1] & 7) << 8) + (self.statdata[2] & 255) * 10

    @property
    def fanspeed(self):
        """requested speed of a FAN element (range 0-7)"""
        if self.type != 'FAN':
            return None
        else:
            return self.statdata[3] & 7

    @property
    def temperature(self):
        """temperature of a THERM element (in celcius)"""
        if self.type != 'THERM':
            return None
        else:
            return self.statdata[2] - 20


class Enclosure(object):
    """main SES2 enclosure device"""

    def __init__(self, device='/dev/ses0'):
        self.devfile = device
        self.open()

    def open(self):
        """open the device file (uses device specified in constructor, or the devfile property)"""
        self.dev = open(self.devfile, 'wb')

    def close(self):
        """close the device file"""
        self.dev.close()

    @property
    def obj_count(self):
        """number of ses objects on this device"""
        return struct.unpack('I', ioctl(self.dev, SESIOC_GETNOBJ, struct.pack('I', 0)))[0]

    @property
    def status_int(self):
        """overall status of the enclosure (as an integer)"""
        s = struct.unpack('B', ioctl(self.dev, SESIOC_GETENCSTAT, struct.pack('B', 0)))[0]
        return s

    @property
    def status(self):
        """overall status of the enclosure"""
        s = struct.unpack('B', ioctl(self.dev, SESIOC_GETENCSTAT, struct.pack('B', 0)))[0]
        r = []
        for i in ENCSTAT:
            if i & s:
                r.append(ENCSTAT[i])

        if not r:
            r.append(ENCSTAT[0])
        return r

    def getobjstat(self, obj_id):
        """get raw object status data (used by ses Object)"""
        objstat_struct = 'iBBBB'
        return struct.unpack(objstat_struct, ioctl(self.dev, SESIOC_GETOBJSTAT, struct.pack(objstat_struct, obj_id, 0, 0, 0, 0)))

    def setobjstat(self, obj_id, data):
        """set raw object status data (used by ses Object)"""
        data = struct.pack('iBBBB', obj_id, data[0], data[1], data[2], data[3])
        ioctl(self.dev, SESIOC_SETOBJSTAT, data)

    @property
    def objects(self):
        """list of objects (with current status)"""
        nobj = self.obj_count
        sesobj_struct = 'III'
        sesobj_size = struct.calcsize(sesobj_struct)
        data = ioctl(self.dev, SESIOC_GETOBJMAP, struct.pack(sesobj_struct, 0, 0, 0) * nobj)
        r = []
        for i in range(0, nobj):
            objdata = struct.unpack(sesobj_struct, data[i * sesobj_size:i * sesobj_size + sesobj_size])
            obj = Object(objdata, self)
            obj.updatestatus()
            r.append(obj)

        if platform.system() == 'FreeBSD' and platform.release() == '9.2-RELEASE':
            t = 0
            for i in range(0, len(r)):
                if not r[i].object_type == t:
                    t = r[i].object_type
                    r[i].object_type = 0
                else:
                    t = r[i].object_type

        return r