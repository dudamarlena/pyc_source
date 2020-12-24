# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ftd2xx\ftd2xx.py
# Compiled at: 2019-09-26 14:10:14
# Size of source mod 2**32: 14849 bytes
"""
Module for accessing functions from FTD2XX in an easier to use
_pythonic_ way. For full documentation please refer to the FTDI
Programming Guide. This module is based on Pablo Bleyers d2xx module,
except this uses ctypes instead of an extension approach.
"""
from __future__ import absolute_import
from builtins import range
from builtins import object
import sys
if sys.platform == 'win32':
    from . import _ftd2xx as _ft
else:
    if sys.platform.startswith('linux'):
        from . import _ftd2xx_linux as _ft
    else:
        if sys.platform == 'darwin':
            from . import _ftd2xx_darwin as _ft
        else:
            import ctypes as c
            from .defines import *
            ft_program_data = _ft.ft_program_data
            msgs = [
             'OK', 'INVALID_HANDLE', 'DEVICE_NOT_FOUND', 'DEVICE_NOT_OPENED',
             'IO_ERROR', 'INSUFFICIENT_RESOURCES', 'INVALID_PARAMETER',
             'INVALID_BAUD_RATE', 'DEVICE_NOT_OPENED_FOR_ERASE',
             'DEVICE_NOT_OPENED_FOR_WRITE', 'FAILED_TO_WRITE_DEVICE0',
             'EEPROM_READ_FAILED', 'EEPROM_WRITE_FAILED', 'EEPROM_ERASE_FAILED',
             'EEPROM_NOT_PRESENT', 'EEPROM_NOT_PROGRAMMED', 'INVALID_ARGS',
             'NOT_SUPPORTED', 'OTHER_ERROR']

            class DeviceError(Exception):
                __doc__ = 'Exception class for status messages'

                def __init__(self, msgnum):
                    self.message = msgs[msgnum]

                def __str__(self):
                    return self.message


            def call_ft(function, *args):
                """Call an FTDI function and check the status. Raise exception on error"""
                status = function(*args)
                if status != _ft.FT_OK:
                    raise DeviceError(status)


            def listDevices(flags=0):
                """Return a list of serial numbers(default), descriptions or
    locations (Windows only) of the connected FTDI devices depending on value
    of flags"""
                n = _ft.DWORD()
                call_ft(_ft.FT_ListDevices, c.byref(n), None, _ft.DWORD(LIST_NUMBER_ONLY))
                devcount = n.value
                if devcount:
                    bd = [c.c_buffer(MAX_DESCRIPTION_SIZE) for i in range(devcount)] + [
                     None]
                    ba = (c.c_char_p * (devcount + 1))()
                    for i in range(devcount):
                        ba[i] = c.cast(bd[i], c.c_char_p)

                    call_ft(_ft.FT_ListDevices, ba, c.byref(n), _ft.DWORD(LIST_ALL | flags))
                    return [res for res in ba[:devcount]]
                return


            def getLibraryVersion():
                """Return a long representing library version"""
                m = _ft.DWORD()
                call_ft(_ft.FT_GetLibraryVersion, c.byref(m))
                return m.value


            def createDeviceInfoList():
                """Create the internal device info list and return number of entries"""
                m = _ft.DWORD()
                call_ft(_ft.FT_CreateDeviceInfoList, c.byref(m))
                return m.value


            def getDeviceInfoDetail(devnum=0, update=True):
                """Get an entry from the internal device info list. Set update to
    False to avoid a slow call to createDeviceInfoList."""
                f = _ft.DWORD()
                t = _ft.DWORD()
                i = _ft.DWORD()
                l = _ft.DWORD()
                h = _ft.FT_HANDLE()
                n = c.c_buffer(MAX_DESCRIPTION_SIZE)
                d = c.c_buffer(MAX_DESCRIPTION_SIZE)
                if update:
                    createDeviceInfoList()
                call_ft(_ft.FT_GetDeviceInfoDetail, _ft.DWORD(devnum), c.byref(f), c.byref(t), c.byref(i), c.byref(l), n, d, c.byref(h))
                return {'index':devnum,  'flags':f.value,  'type':t.value,  'id':i.value, 
                 'location':l.value,  'serial':n.value,  'description':d.value, 
                 'handle':h}


            def open(dev=0):
                """Open a handle to a usb device by index and return an FTD2XX instance for
    it"""
                h = _ft.FT_HANDLE()
                call_ft(_ft.FT_Open, dev, c.byref(h))
                return FTD2XX(h)


            def openEx(id_str, flags=OPEN_BY_SERIAL_NUMBER):
                """Open a handle to a usb device by serial number(default), description or
    location(Windows only) depending on value of flags and return an FTD2XX
    instance for it"""
                h = _ft.FT_HANDLE()
                call_ft(_ft.FT_OpenEx, id_str, _ft.DWORD(flags), c.byref(h))
                return FTD2XX(h)


            if sys.platform == 'win32':
                from win32con import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING

                def w32CreateFile(name, access=GENERIC_READ | GENERIC_WRITE, flags=OPEN_BY_SERIAL_NUMBER):
                    return FTD2XX(_ft.FT_W32_CreateFile(_ft.STRING(name), _ft.DWORD(access), _ft.DWORD(0), None, _ft.DWORD(OPEN_EXISTING), _ft.DWORD(flags), _ft.HANDLE(0)))


            else:

                def getVIDPID():
                    """Linux only. Get the VID and PID of the device"""
                    vid = _ft.DWORD()
                    pid = _ft.DWORD()
                    call_ft(_ft.FT_GetVIDPID, c.byref(vid), c.byref(pid))
                    return (vid.value, pid.value)


                def setVIDPID(vid, pid):
                    """Linux only. Set the VID and PID of the device"""
                    call_ft(_ft.FT_SetVIDPID, _ft.DWORD(vid), _ft.DWORD(pid))


            class FTD2XX(object):
                __doc__ = 'Class for communicating with an FTDI device'

                def __init__(self, handle, update=True):
                    """Create an instance of the FTD2XX class with the given device handle
        and populate the device info in the instance dictionary. Set
        update to False to avoid a slow call to createDeviceInfoList."""
                    self.handle = handle
                    self.status = 1
                    if update:
                        createDeviceInfoList()
                    self.__dict__.update(self.getDeviceInfo())

                def close(self):
                    """Close the device handle"""
                    call_ft(_ft.FT_Close, self.handle)
                    self.status = 0

                def read(self, nchars, raw=True):
                    """Read up to nchars bytes of data from the device. Can return fewer if
        timedout. Use getQueueStatus to find how many bytes are available"""
                    b_read = _ft.DWORD()
                    b = c.c_buffer(nchars)
                    call_ft(_ft.FT_Read, self.handle, b, nchars, c.byref(b_read))
                    if raw:
                        return b.raw[:b_read.value]
                    return b.value[:b_read.value]

                def write(self, data):
                    """Send the data to the device. Data must be a string representing the
        bytes to be sent"""
                    w = _ft.DWORD()
                    call_ft(_ft.FT_Write, self.handle, data, len(data), c.byref(w))
                    return w.value

                def ioctl(self):
                    """Not implemented"""
                    pass

                def setBaudRate(self, baud):
                    """Set the baud rate"""
                    call_ft(_ft.FT_SetBaudRate, self.handle, _ft.DWORD(baud))

                def setDivisor(self, div):
                    """Set the clock divider. The clock will be set to 6e6/(div + 1)."""
                    call_ft(_ft.FT_SetDivisor, self.handle, _ft.USHORT(div))

                def setDataCharacteristics(self, wordlen, stopbits, parity):
                    """Set the data characteristics for UART"""
                    call_ft(_ft.FT_SetDataCharacteristics, self.handle, _ft.UCHAR(wordlen), _ft.UCHAR(stopbits), _ft.UCHAR(parity))

                def setFlowControl(self, flowcontrol, xon=-1, xoff=-1):
                    if flowcontrol == FLOW_XON_XOFF:
                        if xon == -1 or xoff == -1:
                            raise ValueError
                    call_ft(_ft.FT_SetFlowControl, self.handle, _ft.USHORT(flowcontrol), _ft.UCHAR(xon), _ft.UCHAR(xoff))

                def resetDevice(self):
                    """Reset the device"""
                    call_ft(_ft.FT_ResetDevice, self.handle)

                def setDtr(self):
                    call_ft(_ft.FT_SetDtr, self.handle)

                def clrDtr(self):
                    call_ft(_ft.FT_ClrDtr, self.handle)

                def setRts(self):
                    call_ft(_ft.FT_SetRts, self.handle)

                def clrRts(self):
                    call_ft(_ft.FT_ClrRts, self.handle)

                def getModemStatus(self):
                    m = _ft.DWORD()
                    call_ft(_ft.FT_GetModemStatus, self.handle, c.byref(m))
                    return m.value

                def setChars(self, evch, evch_en, erch, erch_en):
                    call_ft(_ft.FT_SetChars, self.handle, _ft.UCHAR(evch), _ft.UCHAR(evch_en), _ft.UCHAR(erch), _ft.UCHAR(erch_en))

                def purge(self, mask=0):
                    if not mask:
                        mask = PURGE_RX | PURGE_TX
                    call_ft(_ft.FT_Purge, self.handle, _ft.DWORD(mask))

                def setTimeouts(self, read, write):
                    call_ft(_ft.FT_SetTimeouts, self.handle, _ft.DWORD(read), _ft.DWORD(write))

                def setDeadmanTimeout(self, timeout):
                    call_ft(_ft.FT_SetDeadmanTimeout, self.handle, _ft.DWORD(timeout))

                def getQueueStatus(self):
                    """Get number of bytes in receive queue."""
                    rxQAmount = _ft.DWORD()
                    call_ft(_ft.FT_GetQueueStatus, self.handle, c.byref(rxQAmount))
                    return rxQAmount.value

                def setEventNotification(self, evtmask, evthandle):
                    call_ft(_ft.FT_SetEventNotification, self.handle, _ft.DWORD(evtmask), _ft.HANDLE(evthandle))

                def getStatus(self):
                    """Return a 3-tuple of rx queue bytes, tx queue bytes and event
        status"""
                    rxQAmount = _ft.DWORD()
                    txQAmount = _ft.DWORD()
                    evtStatus = _ft.DWORD()
                    call_ft(_ft.FT_GetStatus, self.handle, c.byref(rxQAmount), c.byref(txQAmount), c.byref(evtStatus))
                    return (rxQAmount.value, txQAmount.value, evtStatus.value)

                def setBreakOn(self):
                    call_ft(_ft.FT_SetBreakOn, self.handle)

                def setBreakOff(self):
                    call_ft(_ft.FT_SetBreakOff, self.handle)

                def setWaitMask(self, mask):
                    call_ft(_ft.FT_SetWaitMask, self.handle, _ft.DWORD(mask))

                def waitOnMask(self):
                    mask = _ft.DWORD()
                    call_ft(_ft.FT_WaitOnMask, self.handle, c.byref(mask))
                    return mask.value

                def getEventStatus(self):
                    evtStatus = _ft.DWORD()
                    call_ft(_ft.FT_GetEventStatus, self.handle, c.byref(evtStatus))
                    return evtStatus.value

                def setLatencyTimer(self, latency):
                    call_ft(_ft.FT_SetLatencyTimer, self.handle, _ft.UCHAR(latency))

                def getLatencyTimer(self):
                    latency = _ft.UCHAR()
                    call_ft(_ft.FT_GetLatencyTimer, self.handle, c.byref(latency))
                    return latency.value

                def setBitMode(self, mask, enable):
                    call_ft(_ft.FT_SetBitMode, self.handle, _ft.UCHAR(mask), _ft.UCHAR(enable))

                def getBitMode(self):
                    mask = _ft.UCHAR()
                    call_ft(_ft.FT_GetBitMode, self.handle, c.byref(mask))
                    return mask.value

                def setUSBParameters(self, in_tx_size, out_tx_size=0):
                    call_ft(_ft.FT_SetUSBParameters, self.handle, _ft.ULONG(in_tx_size), _ft.ULONG(out_tx_size))

                def getDeviceInfo(self):
                    """Returns a dictionary describing the device. """
                    deviceType = _ft.DWORD()
                    deviceId = _ft.DWORD()
                    desc = c.c_buffer(MAX_DESCRIPTION_SIZE)
                    serial = c.c_buffer(MAX_DESCRIPTION_SIZE)
                    call_ft(_ft.FT_GetDeviceInfo, self.handle, c.byref(deviceType), c.byref(deviceId), serial, desc, None)
                    return {'type':deviceType.value,  'id':deviceId.value,  'description':desc.value, 
                     'serial':serial.value}

                def stopInTask(self):
                    call_ft(_ft.FT_StopInTask, self.handle)

                def restartInTask(self):
                    call_ft(_ft.FT_RestartInTask, self.handle)

                def setRestPipeRetryCount(self, count):
                    call_ft(_ft.FT_SetResetPipeRetryCount, self.handle, _ft.DWORD(count))

                def resetPort(self):
                    call_ft(_ft.FT_ResetPort, self.handle)

                def cyclePort(self):
                    call_ft(_ft.FT_CyclePort, self.handle)

                def getDriverVersion(self):
                    drvver = _ft.DWORD()
                    call_ft(_ft.FT_GetDriverVersion, self.handle, c.byref(drvver))
                    return drvver.value

                def getComPortNumber(self):
                    """Return a long representing the COM port number"""
                    m = _ft.LONG()
                    call_ft(_ft.FT_GetComPortNumber, self.handle, c.byref(m))
                    return m.value

                def eeProgram(self, progdata=None, *args, **kwds):
                    """Program the EEPROM with custom data. If SerialNumber is null, a new
        serial number is generated from ManufacturerId"""
                    if progdata is None:
                        progdata = (_ft.ft_program_data)(**kwds)
                    progdata.Signature1 = _ft.DWORD(0)
                    progdata.Signature2 = _ft.DWORD(4294967295)
                    progdata.Version = _ft.DWORD(2)
                    call_ft(_ft.FT_EE_Program, self.handle, progdata)

                def eeRead(self):
                    """Get the program information from the EEPROM"""
                    progdata = _ft.ft_program_data(Signature1=0,
                      Signature2=4294967295,
                      Version=2,
                      Manufacturer=(c.cast(c.c_buffer(256), c.c_char_p)),
                      ManufacturerId=(c.cast(c.c_buffer(256), c.c_char_p)),
                      Description=(c.cast(c.c_buffer(256), c.c_char_p)),
                      SerialNumber=(c.cast(c.c_buffer(256), c.c_char_p)))
                    call_ft(_ft.FT_EE_Read, self.handle, c.byref(progdata))
                    return progdata

                def eeUASize(self):
                    """Get the EEPROM user area size"""
                    uasize = _ft.DWORD()
                    call_ft(_ft.FT_EE_UASize, self.handle, c.byref(uasize))
                    return uasize.value

                def eeUAWrite(self, data):
                    """Write data to the EEPROM user area. data must be a string with
        appropriate byte values"""
                    call_ft(_ft.FT_EE_UAWrite, self.handle, c.cast(data, _ft.PUCHAR), len(data))

                def eeUARead(self, b_to_read):
                    """Read b_to_read bytes from the EEPROM user area"""
                    b_read = _ft.DWORD()
                    buf = c.c_buffer(b_to_read)
                    call_ft(_ft.FT_EE_UARead, self.handle, c.cast(buf, _ft.PUCHAR), b_to_read, c.byref(b_read))
                    return buf.value[:b_read.value]


            __all__ = [
             'call_ft', 'listDevices', 'getLibraryVersion',
             'createDeviceInfoList', 'getDeviceInfoDetail', 'open',
             'openEx', 'FTD2XX',
             'DeviceError', 'ft_program_data']
            if sys.platform == 'win32':
                __all__ += ['w32CreateFile']
            else:
                __all__ += ['getVIDPID', 'setVIDPID']