# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/SerialDevice.py
# Compiled at: 2018-12-11 15:31:14
# Size of source mod 2**32: 1750 bytes
import asyncio, typing
from asyncinit import asyncinit
import serial_asyncio
import pywavez.SerialDeviceBase as SerialDeviceBase

@asyncinit
class SerialDevice(SerialDeviceBase):

    async def __init__(self, device):
        super().__init__()
        loop = asyncio.get_event_loop()
        self._SerialDevice__reader = asyncio.StreamReader(loop=loop)
        transport, protocol = await serial_asyncio.create_serial_connection(loop=loop,
          protocol_factory=(lambda : asyncio.StreamReaderProtocol((self._SerialDevice__reader),
          loop=loop)),
          url=device,
          baudrate=115200,
          rtscts=True)
        self._SerialDevice__writer = asyncio.StreamWriter(transport, protocol, self._SerialDevice__reader, loop)
        self._SerialDevice__serial = transport.serial
        self._SerialDevice__writeLock = asyncio.Lock()
        self._SerialDevice__readerTask = asyncio.create_task(self._SerialDevice__readerImpl())

    async def sendBreak(self) -> bool:
        async with self._SerialDevice__writeLock:
            self._SerialDevice__serial.break_condition = True
            await asyncio.sleep(0.25)
            self._SerialDevice__serial.break_condition = False
        return True

    async def __readerImpl(self) -> None:
        while True:
            r = await self._SerialDevice__reader.read(1024)
            if not r:
                break
            self._receivedData += r
            self._notify()

        self._readEOF = True
        self._notify()

    async def send(self, data: typing.ByteString) -> None:
        async with self._SerialDevice__writeLock:
            self._SerialDevice__writer.write(data)
            await self._SerialDevice__writer.drain()

    async def close(self) -> None:
        self._SerialDevice__readerTask.cancel()
        self._SerialDevice__writer.close()
        await self._SerialDevice__writer.wait_closed()