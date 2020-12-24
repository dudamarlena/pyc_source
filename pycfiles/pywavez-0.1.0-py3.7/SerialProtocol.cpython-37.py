# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/SerialProtocol.py
# Compiled at: 2019-12-28 09:47:25
# Size of source mod 2**32: 7329 bytes
"""
This module implements the serial ZWave protocol as described in
https://web.archive.org/web/20181103092326/https://www.silabs.com/documents/login/user-guides/INS12350-Serial-API-Host-Appl.-Prg.-Guide.pdf
"""
import asyncio, enum, logging, time, typing
from .SerialDeviceBase import SerialDeviceBase
from .util import waitForOne, spawnTask

class FrameType(enum.Enum):
    SOF = 1
    ACK = 6
    NAK = 21
    CAN = 24


FrameType.values = frozenset((e.value for e in FrameType))

def calcChecksum(data: typing.ByteString) -> int:
    if len(data) > 255:
        raise Exception('bytearray too large')
    val = 255 ^ len(data) + 1 & 255
    for b in data:
        val ^= b

    return val


def frameMessage(payload: typing.ByteString) -> bytearray:
    return bytearray((FrameType.SOF.value, len(payload) + 1)) + payload + bytearray((calcChecksum(payload),))


class SerialProtocol:

    def __init__(self, device: SerialDeviceBase) -> None:
        self._SerialProtocol__dev = device
        self._SerialProtocol__receivedMsgs = []
        self._SerialProtocol__readerFinished = False
        self._SerialProtocol__readerEvent = asyncio.Event()
        self._SerialProtocol__sendMsgQueue = []
        self._SerialProtocol__sendMsgEvent = asyncio.Event()
        self._SerialProtocol__idleEvent = asyncio.Event()
        self._SerialProtocol__task = spawnTask(self._SerialProtocol__taskImpl())
        self._SerialProtocol__task.add_done_callback(self._SerialProtocol__setReaderFinished)

    def send(self, msg):
        fut = asyncio.Future()
        self._SerialProtocol__sendMsgQueue.append((msg, fut))
        self._SerialProtocol__sendMsgEvent.set()
        return fut

    def messageReady(self):
        return self._SerialProtocol__receivedMsgs or self._SerialProtocol__readerFinished

    async def waitForMessage(self):
        while not self.messageReady():
            await self._SerialProtocol__readerEvent.wait()

    @property
    def idle(self):
        return self._SerialProtocol__idleEvent.is_set()

    def waitForIdleState(self):
        return self._SerialProtocol__idleEvent.wait()

    async def getMessage(self, timeout: typing.Optional[float]=None) -> typing.Optional[bytearray]:
        if self._SerialProtocol__receivedMsgs:
            msg = self._SerialProtocol__receivedMsgs.pop(0)
            if not self._SerialProtocol__receivedMsgs:
                if not self._SerialProtocol__readerFinished:
                    self._SerialProtocol__readerEvent.clear()
            return msg
        if timeout is not None:
            expire = time.monotonic() + timeout
        while 1:
            if not self._SerialProtocol__readerFinished:
                try:
                    await asyncio.wait_for(self._SerialProtocol__readerEvent.wait(), None if timeout is None else expire - time.monotonic())
                except asyncio.TimeoutError:
                    return

                if self._SerialProtocol__receivedMsgs:
                    msg = self._SerialProtocol__receivedMsgs.pop(0)
                    if not self._SerialProtocol__receivedMsgs:
                        if not self._SerialProtocol__readerFinished:
                            self._SerialProtocol__readerEvent.clear()
                    return msg
        else:
            raise StopIteration

    def __iter__(self):
        return self

    async def __next__(self) -> bytearray:
        while self._SerialProtocol__receivedMsgs:
            msg = self._SerialProtocol__receivedMsgs.pop(0)
            if not self._SerialProtocol__receivedMsgs:
                if not self._SerialProtocol__readerFinished:
                    self._SerialProtocol__readerEvent.clear()
            return msg
            if self._SerialProtocol__readerFinished:
                raise StopIteration
            await self._SerialProtocol__readerEvent.wait()

    async def __taskImpl(self):
        await self._SerialProtocol__dev.sendBreak()
        await asyncio.sleep(0.5)
        await self._SerialProtocol__sendNak()
        while True:
            self._SerialProtocol__idleEvent.set()
            await waitForOne(self._SerialProtocol__dev.waitForData(), self._SerialProtocol__sendMsgEvent.wait())
            self._SerialProtocol__idleEvent.clear()
            await self._SerialProtocol__doStuff()

    async def __doStuff(self):
        if self._SerialProtocol__dev.hasData():
            c = self._SerialProtocol__dev.takeByte()
            if c != FrameType.SOF.value:
                if c not in FrameType.values:
                    return logging.warning(f"Skipped byte 0x{c:02x} while expecting SOF")
                return logging.warning(f"Skipped {FrameType(c)} while expecting SOF")
            return await self._SerialProtocol__receiveMsg()
        if self._SerialProtocol__sendMsgQueue:
            await self._SerialProtocol__sendMsg()

    async def __receiveMsg(self, *, cancel=False):
        expires = time.monotonic() + 1.5
        try:
            await asyncio.wait_for(self._SerialProtocol__dev.waitForData(), 1.5)
        except asyncio.TimeoutError:
            logging.warning('Timeout while receiving message (1)')
            return
        else:
            length = self._SerialProtocol__dev.takeByte() or 256
        try:
            await asyncio.wait_for(self._SerialProtocol__dev.waitForData(length), expires - time.monotonic())
        except asyncio.TimeoutError:
            return logging.warning('Timeout while receiving message (1)')
        else:
            payload = self._SerialProtocol__dev.takeSomeData(length)
            chksum = payload.pop()
            if cancel:
                await self._SerialProtocol__sendCan()
            else:
                if calcChecksum(payload) == chksum:
                    await self._SerialProtocol__sendAck()
                    self._SerialProtocol__receivedMsgs.append(payload)
                    self._SerialProtocol__readerEvent.set()
                else:
                    logging.warning('Checksum mismatch')
                    await self._SerialProtocol__sendNak()

    async def __sendMsg--- This code section failed: ---

 L. 174         0  SETUP_LOOP           48  'to 48'
              2_0  COME_FROM            30  '30'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _SerialProtocol__sendMsgQueue
                6  POP_JUMP_IF_FALSE    36  'to 36'

 L. 175         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _SerialProtocol__sendMsgQueue
               12  LOAD_METHOD              pop
               14  LOAD_CONST               0
               16  CALL_METHOD_1         1  '1 positional argument'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'msg'
               22  STORE_FAST               'fut'

 L. 176        24  LOAD_FAST                'fut'
               26  LOAD_METHOD              cancelled
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  POP_JUMP_IF_TRUE      2  'to 2'

 L. 177        32  BREAK_LOOP       
               34  JUMP_BACK             2  'to 2'
             36_0  COME_FROM             6  '6'
               36  POP_BLOCK        

 L. 179        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _SerialProtocol__sendMsgEvent
               42  LOAD_METHOD              clear
               44  CALL_METHOD_0         0  '0 positional arguments'
               46  RETURN_VALUE     
             48_0  COME_FROM_LOOP        0  '0'

 L. 180     48_50  SETUP_FINALLY       334  'to 334'
               52  SETUP_EXCEPT        284  'to 284'

 L. 181        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _SerialProtocol__send
               58  LOAD_FAST                'msg'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  POP_TOP          

 L. 182        70  LOAD_GLOBAL              time
               72  LOAD_METHOD              monotonic
               74  CALL_METHOD_0         0  '0 positional arguments'
               76  LOAD_CONST               1.6
               78  BINARY_ADD       
               80  STORE_FAST               'expires'

 L. 183        82  SETUP_LOOP          280  'to 280'

 L. 184        84  LOAD_FAST                'expires'
               86  LOAD_GLOBAL              time
               88  LOAD_METHOD              monotonic
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  BINARY_SUBTRACT  
               94  STORE_FAST               'timeout'

 L. 185        96  LOAD_FAST                'timeout'
               98  LOAD_CONST               0
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 186       104  LOAD_GLOBAL              asyncio
              106  LOAD_METHOD              TimeoutError
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           102  '102'

 L. 187       112  LOAD_GLOBAL              asyncio
              114  LOAD_METHOD              wait_for
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _SerialProtocol__dev
              120  LOAD_METHOD              waitForData
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  LOAD_FAST                'timeout'
              126  CALL_METHOD_2         2  '2 positional arguments'
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  POP_TOP          

 L. 188       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _SerialProtocol__dev
              140  LOAD_METHOD              takeByte
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  STORE_FAST               'c'

 L. 189       146  LOAD_FAST                'c'
              148  LOAD_GLOBAL              FrameType
              150  LOAD_ATTR                ACK
              152  LOAD_ATTR                value
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   168  'to 168'

 L. 190       158  LOAD_FAST                'fut'
              160  LOAD_METHOD              set_result
              162  LOAD_CONST               None
              164  CALL_METHOD_1         1  '1 positional argument'
              166  RETURN_VALUE     
            168_0  COME_FROM           156  '156'

 L. 191       168  LOAD_FAST                'c'
              170  LOAD_GLOBAL              FrameType
              172  LOAD_ATTR                NAK
              174  LOAD_ATTR                value
              176  LOAD_GLOBAL              FrameType
              178  LOAD_ATTR                CAN
              180  LOAD_ATTR                value
              182  BUILD_TUPLE_2         2 
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   206  'to 206'

 L. 192       188  LOAD_GLOBAL              Exception
              190  LOAD_GLOBAL              str
              192  LOAD_GLOBAL              FrameType
              194  LOAD_FAST                'c'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  RAISE_VARARGS_1       1  'exception instance'
              204  JUMP_BACK            84  'to 84'
            206_0  COME_FROM           186  '186'

 L. 193       206  LOAD_FAST                'c'
              208  LOAD_GLOBAL              FrameType
              210  LOAD_ATTR                SOF
              212  LOAD_ATTR                value
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   256  'to 256'

 L. 194       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _SerialProtocol__receiveMsg
              224  LOAD_CONST               True
              226  LOAD_CONST               ('cancel',)
              228  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              230  GET_AWAITABLE    
              232  LOAD_CONST               None
              234  YIELD_FROM       
              236  POP_TOP          

 L. 195       238  LOAD_GLOBAL              Exception
              240  LOAD_GLOBAL              str
              242  LOAD_GLOBAL              FrameType
              244  LOAD_FAST                'c'
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  RAISE_VARARGS_1       1  'exception instance'
              254  JUMP_BACK            84  'to 84'
            256_0  COME_FROM           216  '216'

 L. 197       256  LOAD_GLOBAL              logging
              258  LOAD_METHOD              warning

 L. 198       260  LOAD_STR                 'Skipped byte 0x'
              262  LOAD_FAST                'c'
              264  LOAD_STR                 '02x'
              266  FORMAT_VALUE_ATTR     4  ''
              268  LOAD_STR                 ' while expecting ACK'
              270  BUILD_STRING_3        3 
              272  CALL_METHOD_1         1  '1 positional argument'
              274  POP_TOP          
              276  JUMP_BACK            84  'to 84'
              278  POP_BLOCK        
            280_0  COME_FROM_LOOP       82  '82'
              280  POP_BLOCK        
              282  JUMP_FORWARD        330  'to 330'
            284_0  COME_FROM_EXCEPT     52  '52'

 L. 200       284  DUP_TOP          
              286  LOAD_GLOBAL              Exception
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   328  'to 328'
              294  POP_TOP          
              296  STORE_FAST               'ex'
              298  POP_TOP          
              300  SETUP_FINALLY       316  'to 316'

 L. 201       302  LOAD_FAST                'fut'
              304  LOAD_METHOD              set_exception
              306  LOAD_FAST                'ex'
              308  CALL_METHOD_1         1  '1 positional argument'
              310  POP_TOP          
              312  POP_BLOCK        
              314  LOAD_CONST               None
            316_0  COME_FROM_FINALLY   300  '300'
              316  LOAD_CONST               None
              318  STORE_FAST               'ex'
              320  DELETE_FAST              'ex'
              322  END_FINALLY      
              324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM           290  '290'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM           282  '282'
              330  POP_BLOCK        
              332  LOAD_CONST               None
            334_0  COME_FROM_FINALLY    48  '48'

 L. 203       334  LOAD_FAST                'self'
              336  LOAD_ATTR                _SerialProtocol__sendMsgQueue
          338_340  POP_JUMP_IF_TRUE    352  'to 352'

 L. 204       342  LOAD_FAST                'self'
              344  LOAD_ATTR                _SerialProtocol__sendMsgEvent
              346  LOAD_METHOD              clear
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  POP_TOP          
            352_0  COME_FROM           338  '338'
              352  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 36

    def __sendAck(self) -> typing.Awaitable[None]:
        return self._SerialProtocol__dev.send(bytearray((FrameType.ACK.value,)))

    def __sendNak(self) -> typing.Awaitable[None]:
        return self._SerialProtocol__dev.send(bytearray((FrameType.NAK.value,)))

    def __sendCan(self) -> typing.Awaitable[None]:
        return self._SerialProtocol__dev.send(bytearray((FrameType.CAN.value,)))

    def __send(self, payload: typing.ByteString) -> typing.Awaitable[None]:
        return self._SerialProtocol__dev.send(frameMessage(payload))

    def __setReaderFinished(self, *args):
        self._SerialProtocol__readerFinished = True

    def close(self) -> typing.Awaitable[None]:
        return self._SerialProtocol__dev.close()