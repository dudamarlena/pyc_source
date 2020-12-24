# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/SerialDeviceBase.py
# Compiled at: 2019-12-28 09:47:19
# Size of source mod 2**32: 2269 bytes
import asyncio, typing, re

class SerialDeviceBase:

    def __init__(self):
        self._receivedData = bytearray()
        self._receivedDataNotifications = []
        self._readEOF = False

    def hasData(self) -> bool:
        return bool(self._receivedData)

    def atEOF(self) -> bool:
        return self._readEOF

    def takeAllData(self) -> bytearray:
        data = self._receivedData
        self._receivedData = bytearray()
        return data

    def takeSomeData(self, bytes: int) -> bytearray:
        if bytes > len(self._receivedData):
            raise Exception('not enough data available')
        res = self._receivedData[0:bytes]
        self._receivedData = self._receivedData[bytes:]
        return res

    def takeByte(self) -> int:
        return self._receivedData.pop(0)

    def waitForData(self, bytes=1):
        fut = asyncio.Future()
        if len(self._receivedData) >= bytes:
            fut.set_result(None)
        else:
            self._receivedDataNotifications.append((bytes, fut))
        return fut

    def _notify(self):
        if not self._receivedData:
            return
        notifications = self._receivedDataNotifications
        self._receivedDataNotifications = []
        for b, fut in notifications:
            if not fut.cancelled():
                if len(self._receivedData) >= b:
                    fut.set_result(None)
                elif self._readEOF:
                    fut.set_exception(EOFError())
                else:
                    self._receivedDataNotifications.append((b, fut))

    def __iter__(self):
        return self

    async def __next__(self) -> bytearray:
        while 1:
            await self.waitForData()
            if self.hasData():
                return self.takeAllData()
            if self._readEOF:
                raise StopIteration


def makeSerialDevice(dev) -> typing.Awaitable[SerialDeviceBase]:
    match = re.match('^([\\w\\-\\.:]+):(\\d+)$', dev)
    if match:
        host, port = match.groups()
        port = int(port)
        import pywavez.RemoteSerialDevice as RemoteSerialDevice
        return RemoteSerialDevice(host, port)
    import pywavez.SerialDevice as SerialDevice
    return SerialDevice(dev)